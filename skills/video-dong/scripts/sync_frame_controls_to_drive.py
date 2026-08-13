#!/usr/bin/env python3
"""Sync first/last frame controls with Google Drive through the gws CLI.

The script intentionally performs no delete or trash operation. It uploads or
registers frame references, verifies Drive metadata, and writes a render-ready
manifest for a downstream video generation pipeline.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import mimetypes
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

try:
    from PIL import Image
except ImportError:  # pragma: no cover - the error is reported when a local image is used
    Image = None  # type: ignore[assignment]

IMAGE_MIME_TYPES = {"image/png", "image/jpeg", "image/webp"}
DRIVE_FIELDS = (
    "id,name,mimeType,size,md5Checksum,webViewLink,webContentLink,trashed,"
    "parents,createdTime,modifiedTime"
)


class GwsError(RuntimeError):
    """Raised when a gws command fails or returns invalid JSON."""


DEFAULT_GWS_TIMEOUT = 30.0
DEFAULT_READ_RETRIES = 3


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def parse_json_output(raw: str, command: list[str]) -> dict[str, Any]:
    """Parse gws JSON while tolerating harmless leading/trailing CLI text."""
    raw = raw.strip()
    try:
        value = json.loads(raw)
    except json.JSONDecodeError:
        start = min((index for index in (raw.find("{"), raw.find("[")) if index >= 0), default=-1)
        if start < 0:
            raise GwsError(f"gws returned non-JSON output for {' '.join(command)}: {raw[:500]}")
        try:
            value = json.loads(raw[start:])
        except json.JSONDecodeError as exc:
            raise GwsError(f"Cannot parse gws JSON for {' '.join(command)}: {exc}") from exc
    if not isinstance(value, dict):
        raise GwsError(f"Expected a JSON object from {' '.join(command)}")
    return value


def run_gws(service: str, resource: str, operation: str, *, params: dict[str, Any] | None = None,
            body: dict[str, Any] | None = None, upload: Path | None = None,
            upload_content_type: str | None = None, timeout: float = DEFAULT_GWS_TIMEOUT,
            retries: int = DEFAULT_READ_RETRIES, mutation: bool = False) -> dict[str, Any]:
    command = ["gws", service, resource, operation]
    if params is not None:
        command.extend(["--params", json.dumps(params, ensure_ascii=False, separators=(",", ":"))])
    if body is not None:
        command.extend(["--json", json.dumps(body, ensure_ascii=False, separators=(",", ":"))])
    if upload is not None:
        command.extend(["--upload", str(upload)])
        if upload_content_type:
            command.extend(["--upload-content-type", upload_content_type])

    # Read-only calls may retry with backoff. Mutations are never retried here;
    # a timeout can mean the remote operation succeeded, so the caller must
    # reconcile by idempotency key before attempting another mutation.
    attempts = 1 if mutation else max(1, min(int(retries), 4))
    for attempt in range(attempts):
        try:
            completed = subprocess.run(command, capture_output=True, text=True, check=False, timeout=timeout)
        except subprocess.TimeoutExpired as exc:
            if attempt + 1 < attempts:
                time.sleep(min(2 ** attempt, 4))
                continue
            state = "unknown_after_timeout" if mutation else "timeout"
            raise GwsError(f"{state}: gws command exceeded {timeout:.1f}s: {' '.join(command)}") from exc
        if completed.returncode == 0:
            return parse_json_output(completed.stdout, command)
        detail = (completed.stderr or completed.stdout).strip()
        if attempt + 1 < attempts:
            time.sleep(min(2 ** attempt, 4))
            continue
        raise GwsError(f"gws command failed ({completed.returncode}): {' '.join(command)}\n{detail[:500]}")
    raise GwsError(f"gws command did not complete: {' '.join(command)}")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def local_frame_metadata(path: Path) -> dict[str, Any]:
    if not path.is_file():
        raise ValueError(f"Frame file does not exist: {path}")
    mime_type, _ = mimetypes.guess_type(path.name)
    if mime_type not in IMAGE_MIME_TYPES:
        raise ValueError(f"Unsupported frame type {mime_type!r}; use PNG, JPEG, or WebP: {path}")
    if Image is None:
        raise ValueError("Pillow is required to inspect local frames. Install it with: sudo pip3 install pillow")
    try:
        with Image.open(path) as image:
            image.verify()
        with Image.open(path) as image:
            width, height = image.size
            image_format = image.format
    except Exception as exc:  # Pillow raises different exceptions by format
        raise ValueError(f"Invalid or unreadable image: {path}: {exc}") from exc
    if width < 2 or height < 2:
        raise ValueError(f"Frame is too small: {path} ({width}x{height})")
    return {
        "local_path": str(path.resolve()),
        "name": path.name,
        "mime_type": mime_type,
        "bytes": path.stat().st_size,
        "sha256": sha256_file(path),
        "width": width,
        "height": height,
        "format": image_format,
    }


def get_drive_file(file_id: str) -> dict[str, Any]:
    return run_gws(
        "drive", "files", "get",
        params={"fileId": file_id, "fields": DRIVE_FIELDS},
    )


def create_job_folder(job_id: str, folder_name: str | None, parent_folder_id: str | None) -> dict[str, Any]:
    name = folder_name or f"job-{job_id}-frames"
    if parent_folder_id:
        query = (
            f"name = '{name.replace(chr(39), chr(92) + chr(39))}' and "
            f"'{parent_folder_id}' in parents and "
            "mimeType = 'application/vnd.google-apps.folder' and trashed = false"
        )
        existing = run_gws(
            "drive", "files", "list",
            params={"q": query, "pageSize": 10, "fields": "files(id,name,mimeType,parents,trashed,webViewLink)"},
        ).get("files", [])
        if existing:
            record = dict(existing[0])
            record["_created_by_this_run"] = False
            return record
    body: dict[str, Any] = {"name": name, "mimeType": "application/vnd.google-apps.folder"}
    if parent_folder_id:
        body["parents"] = [parent_folder_id]
    created = run_gws("drive", "files", "create", body=body, mutation=True)
    created["_created_by_this_run"] = True
    return created


def frame_idempotency_key(job_id: str, scene_id: str, label: str, sha256: str) -> str:
    return f"frame-control:{job_id}:{scene_id}:{label}:{sha256}"


def find_existing_frame(folder_id: str, name: str, idempotency_key: str) -> dict[str, Any] | None:
    safe_name = name.replace(chr(39), chr(92) + chr(39))
    safe_description = idempotency_key.replace(chr(39), chr(92) + chr(39))
    query = (
        f"name = '{safe_name}' and '{folder_id}' in parents and trashed = false "
        f"and description = '{safe_description}'"
    )
    response = run_gws(
        "drive", "files", "list",
        params={"q": query, "pageSize": 10, "fields": DRIVE_FIELDS},
    )
    files = response.get("files", [])
    return dict(files[0]) if files else None


def upload_frame(path: Path, folder_id: str, idempotency_key: str) -> dict[str, Any]:
    existing = find_existing_frame(folder_id, path.name, idempotency_key)
    if existing is not None:
        return existing
    metadata = {"name": path.name, "parents": [folder_id], "description": idempotency_key}
    mime_type = mimetypes.guess_type(path.name)[0]
    return run_gws(
        "drive", "files", "create",
        body=metadata,
        upload=path,
        upload_content_type=mime_type,
        mutation=True,
    )


def verify_drive_file(remote: dict[str, Any], local: dict[str, Any] | None = None) -> dict[str, Any]:
    if remote.get("trashed") is True:
        raise ValueError(f"Drive file is already in trash: {remote.get('id')}")
    if remote.get("mimeType") not in IMAGE_MIME_TYPES:
        raise ValueError(
            f"Drive file {remote.get('id')} is not a supported image: {remote.get('mimeType')}"
        )
    if local is not None:
        remote_size = remote.get("size")
        if remote_size is not None and int(remote_size) != local["bytes"]:
            raise ValueError(
                f"Uploaded size mismatch for {local['name']}: local={local['bytes']} remote={remote_size}"
            )
    return {
        "drive_file_id": remote.get("id"),
        "name": remote.get("name"),
        "mime_type": remote.get("mimeType"),
        "bytes": int(remote["size"]) if remote.get("size") is not None else None,
        "md5_checksum": remote.get("md5Checksum"),
        "web_view_link": remote.get("webViewLink"),
        "web_content_link": remote.get("webContentLink"),
        "parents": remote.get("parents", []),
        "trashed": bool(remote.get("trashed", False)),
    }


def resolve_frame(label: str, path: Path | None, file_id: str | None, folder_id: str | None,
                  job_id: str, scene_id: str, dry_run: bool) -> dict[str, Any]:
    if path is None and file_id is None:
        raise ValueError(f"Provide either --{label}-frame PATH or --{label}-frame-file-id ID")
    if path is not None and file_id is not None:
        raise ValueError(f"Use only one of --{label}-frame and --{label}-frame-file-id")

    if file_id:
        if dry_run:
            return {
                "source": "drive_reference",
                "drive_file_id": file_id,
                "verification": "skipped_in_dry_run",
            }
        remote = get_drive_file(file_id)
        verified = verify_drive_file(remote)
        verified["source"] = "drive_reference"
        return verified

    assert path is not None
    local = local_frame_metadata(path)
    idempotency_key = frame_idempotency_key(job_id, scene_id, label, local["sha256"])
    if dry_run:
        local["source"] = "local_upload_preview"
        local["verification"] = "skipped_in_dry_run"
        return local
    if not folder_id:
        raise ValueError("A Drive folder ID is required when uploading local frames")
    uploaded = upload_frame(path, folder_id, idempotency_key)
    remote = get_drive_file(uploaded.get("id", ""))
    verified = verify_drive_file(remote, local)
    verified.update({
        "source": "local_upload",
        "local_path": local["local_path"],
        "sha256": local["sha256"],
        "width": local["width"],
        "height": local["height"],
        "format": local["format"],
        "idempotency_key": idempotency_key,
    })
    return verified


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Upload or register first/last frames in Google Drive using the gws CLI."
    )
    parser.add_argument("--job-id", required=True, help="Stable job identifier")
    parser.add_argument("--scene-id", required=True, help="Scene identifier, e.g. scene-001")
    parser.add_argument("--folder-id", help="Existing Google Drive folder ID for this job")
    parser.add_argument("--create-folder", action="store_true", help="Create a Drive folder when --folder-id is absent")
    parser.add_argument("--folder-name", help="Name for a newly created Drive folder")
    parser.add_argument("--parent-folder-id", help="Optional parent folder ID for a newly created folder")
    parser.add_argument("--first-frame", type=Path, help="Local first-frame image to upload")
    parser.add_argument("--first-frame-file-id", help="Existing Drive file ID for the first frame")
    parser.add_argument("--last-frame", type=Path, help="Local last-frame image to upload")
    parser.add_argument("--last-frame-file-id", help="Existing Drive file ID for the last frame")
    parser.add_argument("--manifest-out", type=Path, default=Path("frame-control-manifest.json"), help="Local manifest output path")
    parser.add_argument("--dry-run", action="store_true", help="Inspect local files but do not call Drive")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        folder_id = args.folder_id
        folder_record: dict[str, Any] | None = None
        if args.create_folder and folder_id:
            raise ValueError("Use either --folder-id or --create-folder, not both")
        if not folder_id and not args.create_folder and not args.dry_run:
            raise ValueError("Provide --folder-id or --create-folder for upload mode")
        if args.create_folder and not args.dry_run:
            folder_record = create_job_folder(args.job_id, args.folder_name, args.parent_folder_id)
            folder_id = folder_record.get("id")
            if not folder_id:
                raise GwsError("Drive folder creation returned no file ID")

        first = resolve_frame("first", args.first_frame, args.first_frame_file_id, folder_id, args.job_id, args.scene_id, args.dry_run)
        last = resolve_frame("last", args.last_frame, args.last_frame_file_id, folder_id, args.job_id, args.scene_id, args.dry_run)

        manifest: dict[str, Any] = {
            "schema_version": "1.0",
            "manifest_type": "first_last_frame_control",
            "job_id": args.job_id,
            "scene_id": args.scene_id,
            "created_at": utc_now(),
            "identity_policy": "preserve_exact_person",
            "continuity_policy": {
                "use_first_frame_as_scene_anchor": True,
                "use_last_frame_as_next_scene_anchor": True,
                "preserve_exact_person": True,
                "allow_face_swap": False,
                "allow_identity_drift": False,
            },
            "drive": {
                "folder_id": folder_id,
                "folder_created_by_this_run": bool(folder_record and folder_record.get("_created_by_this_run")),
                "folder_name": folder_record.get("name") if folder_record else None,
            },
            "frames": {"first": first, "last": last},
            "cleanup": {
                "requested": False,
                "policy": "Do not trash or delete frames from this script; cleanup requires a separate final quality gate.",
            },
            "status": "dry_run" if args.dry_run else "verified",
        }
        args.manifest_out.parent.mkdir(parents=True, exist_ok=True)
        args.manifest_out.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(json.dumps(manifest, ensure_ascii=False, indent=2))
        return 0
    except (GwsError, ValueError, OSError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
