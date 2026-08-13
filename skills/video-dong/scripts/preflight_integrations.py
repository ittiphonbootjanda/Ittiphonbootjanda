#!/usr/bin/env python3
"""Safe, read-only preflight checks for วีดีโด่ง integrations.

The script checks local executables, GitHub auth, Google Drive read-only health,
HTTPS reachability, disk space, and an optional connection manifest. It never
uploads, mutates, trashes, or deletes files. Secrets and command output are not
written to the report.
"""

from __future__ import annotations

import argparse
import hashlib
import ipaddress
import json
import shutil
import socket
import subprocess
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

DEFAULT_URL = "https://www.google.com/generate_204"
DEFAULT_TOOLS = ("python3", "ffmpeg", "ffprobe", "curl", "gws", "gh")


def now_utc() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def redact(text: str) -> str:
    lowered = text.lower()
    if any(token in lowered for token in ("token", "secret", "authorization", "api_key", "apikey", "password")):
        return "redacted-sensitive-output"
    return "redacted"


def run_readonly(command: list[str], timeout: float, attempts: int = 1) -> tuple[str, str]:
    """Run a read-only command with bounded retry; return status and safe detail."""
    attempts = max(1, min(attempts, 4))
    for attempt in range(attempts):
        try:
            completed = subprocess.run(
                command,
                capture_output=True,
                text=True,
                timeout=timeout,
                check=False,
            )
        except subprocess.TimeoutExpired:
            if attempt + 1 < attempts:
                time.sleep(min(2 ** attempt, 4))
                continue
            return "timeout", "command timed out"
        except OSError as exc:
            return "error", type(exc).__name__
        if completed.returncode == 0:
            return "pass", "ok"
        if attempt + 1 < attempts:
            time.sleep(min(2 ** attempt, 4))
            continue
        return "fail", f"exit_code={completed.returncode}; output={redact((completed.stderr or completed.stdout).strip()[:160])}"
    return "unknown_after_timeout", "bounded retry exhausted"


def parse_json_output(raw: str) -> Any:
    raw = raw.strip()
    if not raw:
        raise ValueError("empty JSON output")
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        starts = [index for index in (raw.find("{"), raw.find("[")) if index >= 0]
        if not starts:
            raise
        return json.loads(raw[min(starts):])


def run_json_readonly(command: list[str], timeout: float, attempts: int) -> tuple[str, str, Any | None]:
    for attempt in range(max(1, min(attempts, 4))):
        try:
            completed = subprocess.run(command, capture_output=True, text=True, timeout=timeout, check=False)
        except subprocess.TimeoutExpired:
            if attempt + 1 < attempts:
                time.sleep(min(2 ** attempt, 4))
                continue
            return "timeout", "command timed out", None
        except OSError as exc:
            return "error", type(exc).__name__, None
        if completed.returncode != 0:
            if attempt + 1 < attempts:
                time.sleep(min(2 ** attempt, 4))
                continue
            return "fail", f"exit_code={completed.returncode}; output={redact((completed.stderr or completed.stdout).strip()[:160])}", None
        try:
            return "pass", "ok", parse_json_output(completed.stdout)
        except (ValueError, json.JSONDecodeError) as exc:
            return "fail", f"invalid_json={type(exc).__name__}", None
    return "unknown_after_timeout", "bounded retry exhausted", None


def check_tool(name: str, timeout: float) -> dict[str, Any]:
    path = shutil.which(name)
    if not path:
        return {"id": f"tool:{name}", "kind": "local_tool", "status": "fail", "detail": "not found"}
    # FFmpeg tools use a single-dash version flag; --version returns a
    # non-zero code on the Ubuntu build even though the executable is healthy.
    version_flag = "-version" if name in {"ffmpeg", "ffprobe"} else "--version"
    status, detail = run_readonly([name, version_flag], timeout, attempts=1)
    return {"id": f"tool:{name}", "kind": "local_tool", "status": status, "detail": detail if status != "pass" else "available", "path": path, "version_flag": version_flag}


def check_github(timeout: float) -> dict[str, Any]:
    if not shutil.which("gh"):
        return {"id": "github-auth", "kind": "github", "status": "fail", "detail": "gh not found"}
    status, detail = run_readonly(["gh", "auth", "status"], timeout, attempts=2)
    return {"id": "github-auth", "kind": "github", "status": status, "detail": detail}


def check_drive(timeout: float, attempts: int) -> dict[str, Any]:
    if not shutil.which("gws"):
        return {"id": "google-drive-health", "kind": "storage", "status": "fail", "detail": "gws not found"}
    command = [
        "gws", "drive", "about", "get",
        "--params", json.dumps({"fields": "kind,maxUploadSize,storageQuota"}, separators=(",", ":")),
    ]
    status, detail, payload = run_json_readonly(command, timeout, attempts)
    record: dict[str, Any] = {"id": "google-drive-health", "kind": "storage", "status": status, "detail": detail}
    if status == "pass" and isinstance(payload, dict):
        record["has_drive_about"] = payload.get("kind") == "drive#about"
        quota = payload.get("storageQuota")
        if isinstance(quota, dict):
            # Quota values are operational metadata, not credentials.
            record["quota"] = {
                key: quota.get(key)
                for key in ("limit", "usage", "usageInDrive", "usageInDriveTrash")
                if quota.get(key) is not None
            }
        if record.get("has_drive_about") is not True:
            record["status"] = "fail"
            record["detail"] = "unexpected Drive about response"
    return record


def public_host(hostname: str) -> bool:
    try:
        addresses = {item[4][0] for item in socket.getaddrinfo(hostname, 443, type=socket.SOCK_STREAM)}
    except socket.gaierror:
        return False
    if not addresses:
        return False
    for address in addresses:
        try:
            ip = ipaddress.ip_address(address)
        except ValueError:
            return False
        if not ip.is_global:
            return False
    return True


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req: urllib.request.Request, fp: Any, code: int, msg: str, headers: Any, newurl: str) -> None:
        return None


def check_https(url: str, timeout: float) -> dict[str, Any]:
    from urllib.parse import urljoin, urlparse

    current_url = url
    redirects: list[str] = []
    opener = urllib.request.build_opener(NoRedirect)
    for _ in range(4):
        parsed = urlparse(current_url)
        if parsed.scheme != "https" or not parsed.hostname or not public_host(parsed.hostname):
            return {"id": f"internet:{url}", "kind": "internet", "status": "fail", "detail": "only public HTTPS URLs are allowed", "redirects": redirects}
        request = urllib.request.Request(current_url, method="HEAD", headers={"User-Agent": "video-dong-preflight/1.0"})
        try:
            with opener.open(request, timeout=timeout) as response:
                code = int(response.status)
            return {"id": f"internet:{url}", "kind": "internet", "status": "pass" if 200 <= code < 400 else "fail", "http_status": code, "host": parsed.hostname, "redirects": redirects}
        except urllib.error.HTTPError as exc:
            if exc.code not in {301, 302, 303, 307, 308}:
                return {"id": f"internet:{url}", "kind": "internet", "status": "fail", "http_status": exc.code, "host": parsed.hostname, "redirects": redirects}
            location = exc.headers.get("Location")
            if not location:
                return {"id": f"internet:{url}", "kind": "internet", "status": "fail", "detail": "redirect_without_location", "host": parsed.hostname, "redirects": redirects}
            current_url = urljoin(current_url, location)
            redirects.append(current_url)
            continue
        except (urllib.error.URLError, TimeoutError, OSError) as exc:
            return {"id": f"internet:{url}", "kind": "internet", "status": "fail", "detail": type(exc).__name__, "host": parsed.hostname, "redirects": redirects}
    return {"id": f"internet:{url}", "kind": "internet", "status": "fail", "detail": "too_many_redirects", "redirects": redirects}


def check_disk(path: Path, minimum: int) -> dict[str, Any]:
    try:
        usage = shutil.disk_usage(path)
    except OSError as exc:
        return {"id": "local-disk", "kind": "storage", "status": "fail", "detail": type(exc).__name__}
    return {
        "id": "local-disk",
        "kind": "storage",
        "status": "pass" if usage.free >= minimum else "fail",
        "free_bytes": usage.free,
        "required_free_bytes": minimum,
        "path": str(path.resolve()),
    }


def check_manifest(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {"id": "connection-manifest", "kind": "manifest", "status": "skipped", "detail": "not provided"}
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return {"id": "connection-manifest", "kind": "manifest", "status": "fail", "detail": type(exc).__name__}
    if not isinstance(payload, dict) or not isinstance(payload.get("connections"), list):
        return {"id": "connection-manifest", "kind": "manifest", "status": "fail", "detail": "expected object with connections list"}
    connections = payload["connections"]
    missing = [index for index, item in enumerate(connections) if not isinstance(item, dict) or not item.get("provider") or not item.get("timeout_seconds")]
    return {
        "id": "connection-manifest",
        "kind": "manifest",
        "status": "fail" if missing else "pass",
        "connection_count": len(connections),
        "invalid_entries": missing,
        "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Read-only integration preflight for วีดีโด่ง")
    parser.add_argument("--report-out", type=Path, default=Path("connection-preflight-report.json"))
    parser.add_argument("--connection-manifest", type=Path)
    parser.add_argument("--job-root", type=Path, default=Path.cwd())
    parser.add_argument("--min-free-bytes", type=int, default=2 * 1024 * 1024 * 1024)
    parser.add_argument("--timeout", type=float, default=20.0)
    parser.add_argument("--retries", type=int, default=2)
    parser.add_argument("--url", action="append", dest="urls", help="Public HTTPS URL to health-check; repeatable")
    parser.add_argument("--skip-drive", action="store_true")
    parser.add_argument("--skip-github", action="store_true")
    parser.add_argument("--skip-internet", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    checks: list[dict[str, Any]] = [check_tool(name, args.timeout) for name in DEFAULT_TOOLS]
    if not args.skip_drive:
        checks.append(check_drive(args.timeout, args.retries))
    if not args.skip_github:
        checks.append(check_github(args.timeout))
    if not args.skip_internet:
        for url in args.urls or [DEFAULT_URL]:
            checks.append(check_https(url, args.timeout))
    checks.append(check_disk(args.job_root, args.min_free_bytes))
    if args.connection_manifest:
        checks.append(check_manifest(args.connection_manifest))
    required = [item for item in checks if item.get("status") not in {"pass", "skipped"}]
    report = {
        "schema_version": "1.0",
        "report_type": "connection_preflight",
        "display_name": "วีดีโด่ง",
        "technical_id": "video-dong",
        "created_at": now_utc(),
        "read_only": True,
        "checks": checks,
        "status": "pass" if not required else "fail",
        "failed_check_ids": [item["id"] for item in required],
        "policy": {
            "mutations_performed": False,
            "secrets_written": False,
            "internet_url_policy": "public-https-only",
            "cleanup_allowed": False,
        },
    }
    args.report_out.parent.mkdir(parents=True, exist_ok=True)
    args.report_out.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report["status"] == "pass" else 2


if __name__ == "__main__":
    raise SystemExit(main())
