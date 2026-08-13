#!/usr/bin/env python3
"""Safely fetch an internet asset for วีดีโด่ง.

The downloader is deliberately conservative: HTTPS only, explicit domain
allowlist unless --allow-any-public-domain is supplied, public-IP validation
for every redirect, bounded redirects/bytes, MIME validation, atomic writes,
and a provenance record. It never executes downloaded content.
"""

from __future__ import annotations

import argparse
import hashlib
import ipaddress
import json
import mimetypes
import os
import socket
import sys
import tempfile
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

DEFAULT_TIMEOUT = 20.0
DEFAULT_MAX_BYTES = 25 * 1024 * 1024
DEFAULT_MAX_REDIRECTS = 3
ALLOWED_MIME_PREFIXES = ("image/", "video/", "audio/", "text/")
ALLOWED_EXACT_MIME = {"application/json", "application/pdf", "application/octet-stream"}


class FetchError(RuntimeError):
    """Raised when an asset fails a safe-fetch policy."""


def now_utc() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def public_host(hostname: str) -> set[str]:
    try:
        addresses = {item[4][0] for item in socket.getaddrinfo(hostname, 443, type=socket.SOCK_STREAM)}
    except socket.gaierror as exc:
        raise FetchError(f"DNS resolution failed for {hostname}") from exc
    if not addresses:
        raise FetchError(f"No address resolved for {hostname}")
    for address in addresses:
        try:
            ip = ipaddress.ip_address(address)
        except ValueError as exc:
            raise FetchError(f"Invalid resolved address for {hostname}") from exc
        if not ip.is_global:
            raise FetchError(f"Host resolves to non-public address: {hostname}")
    return addresses


def normalize_allowed_domains(values: list[str]) -> set[str]:
    result: set[str] = set()
    for value in values:
        domain = value.lower().strip().rstrip(".")
        if not domain or "://" in domain or "/" in domain:
            raise FetchError(f"Invalid --allowed-domain: {value}")
        result.add(domain)
    return result


def validate_url(url: str, allowed_domains: set[str], allow_any_public_domain: bool) -> str:
    parsed = urllib.parse.urlparse(url)
    if parsed.scheme != "https" or not parsed.hostname:
        raise FetchError("Only HTTPS URLs with a hostname are allowed")
    if parsed.username or parsed.password:
        raise FetchError("URLs containing username/password are not allowed")
    if parsed.port not in (None, 443):
        raise FetchError("Only the default HTTPS port is allowed")
    host = parsed.hostname.lower().rstrip(".")
    if not allow_any_public_domain and not any(host == domain or host.endswith("." + domain) for domain in allowed_domains):
        raise FetchError(f"Host is not in the explicit allowlist: {host}")
    public_host(host)
    return urllib.parse.urlunparse(("https", host, parsed.path or "/", "", parsed.query, ""))


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req: urllib.request.Request, fp: Any, code: int, msg: str, headers: Any, newurl: str) -> None:
        return None


def content_type(headers: Any) -> str:
    value = headers.get("Content-Type", "").split(";", 1)[0].strip().lower()
    if not value:
        raise FetchError("Response did not provide a Content-Type")
    if not (value.startswith(ALLOWED_MIME_PREFIXES) or value in ALLOWED_EXACT_MIME):
        raise FetchError(f"Disallowed Content-Type: {value}")
    return value


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def fetch(url: str, output: Path, provenance_out: Path, args: argparse.Namespace) -> dict[str, Any]:
    allowed_domains = normalize_allowed_domains(args.allowed_domain or [])
    if not allowed_domains and not args.allow_any_public_domain:
        raise FetchError("Provide --allowed-domain or explicitly use --allow-any-public-domain")
    current_url = validate_url(url, allowed_domains, args.allow_any_public_domain)
    redirects: list[str] = []
    opener = urllib.request.build_opener(NoRedirect)
    request_headers = {"User-Agent": "video-dong-asset-fetch/1.0", "Accept": args.accept}

    output.parent.mkdir(parents=True, exist_ok=True)
    if output.exists() and not args.overwrite:
        raise FetchError(f"Output already exists; use --overwrite explicitly: {output}")

    response = None
    try:
        for _ in range(args.max_redirects + 1):
            request = urllib.request.Request(current_url, method="GET", headers=request_headers)
            try:
                response = opener.open(request, timeout=args.timeout)
                break
            except urllib.error.HTTPError as exc:
                if exc.code not in {301, 302, 303, 307, 308}:
                    raise FetchError(f"HTTP error {exc.code}") from exc
                location = exc.headers.get("Location")
                if not location:
                    raise FetchError(f"Redirect {exc.code} did not provide Location") from exc
                next_url = urllib.parse.urljoin(current_url, location)
                next_url = validate_url(next_url, allowed_domains, args.allow_any_public_domain)
                redirects.append(next_url)
                current_url = next_url
        else:
            raise FetchError(f"Too many redirects; limit is {args.max_redirects}")

        if response is None:
            raise FetchError("No response received")
        status = int(getattr(response, "status", 200))
        if not 200 <= status < 300:
            raise FetchError(f"Unexpected HTTP status {status}")
        mime = content_type(response.headers)
        declared_length = response.headers.get("Content-Length")
        if declared_length and int(declared_length) > args.max_bytes:
            raise FetchError("Content-Length exceeds configured maximum")

        fd, temp_name = tempfile.mkstemp(prefix=".video-dong-", dir=str(output.parent))
        os.close(fd)
        temp_path = Path(temp_name)
        total = 0
        try:
            with temp_path.open("wb") as handle:
                while True:
                    chunk = response.read(min(1024 * 1024, args.max_bytes - total + 1))
                    if not chunk:
                        break
                    total += len(chunk)
                    if total > args.max_bytes:
                        raise FetchError("Downloaded content exceeds configured maximum")
                    handle.write(chunk)
                handle.flush()
                os.fsync(handle.fileno())
            digest = sha256_file(temp_path)
            if output.exists() and args.overwrite:
                output.unlink()
            os.replace(temp_path, output)
        finally:
            temp_path.unlink(missing_ok=True)
    finally:
        if response is not None:
            response.close()

    record: dict[str, Any] = {
        "schema_version": "1.0",
        "record_type": "internet_asset_provenance",
        "display_name": "วีดีโด่ง",
        "technical_id": "video-dong",
        "source_url": url,
        "final_url": current_url,
        "redirects": redirects,
        "accessed_at": now_utc(),
        "publisher": args.publisher,
        "license": args.license,
        "source_kind": args.source_kind,
        "output_path": str(output.resolve()),
        "content_type": mime,
        "bytes": total,
        "sha256": digest,
        "policy": {
            "https_only": True,
            "allowlist_enforced": not args.allow_any_public_domain,
            "max_redirects": args.max_redirects,
            "max_bytes": args.max_bytes,
            "executed_download": False,
        },
    }
    provenance_out.parent.mkdir(parents=True, exist_ok=True)
    provenance_out.write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return record


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Safely fetch a public internet asset for วีดีโด่ง")
    parser.add_argument("--url", required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--provenance-out", type=Path, required=True)
    parser.add_argument("--allowed-domain", action="append", help="Allowed domain; repeatable")
    parser.add_argument("--allow-any-public-domain", action="store_true", help="Explicitly allow any public HTTPS domain")
    parser.add_argument("--max-bytes", type=int, default=DEFAULT_MAX_BYTES)
    parser.add_argument("--max-redirects", type=int, default=DEFAULT_MAX_REDIRECTS)
    parser.add_argument("--timeout", type=float, default=DEFAULT_TIMEOUT)
    parser.add_argument("--accept", default="image/*,video/*,audio/*,text/*,application/json,application/pdf")
    parser.add_argument("--publisher", default="")
    parser.add_argument("--license", default="unknown")
    parser.add_argument("--source-kind", default="reference")
    parser.add_argument("--overwrite", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.max_bytes <= 0 or not 0 <= args.max_redirects <= 10 or args.timeout <= 0:
        print("ERROR: invalid size, redirect, or timeout limits", file=sys.stderr)
        return 2
    try:
        record = fetch(args.url, args.out, args.provenance_out, args)
    except (FetchError, OSError, ValueError) as exc:
        print(f"ERROR: {type(exc).__name__}: {exc}", file=sys.stderr)
        return 2
    print(json.dumps(record, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
