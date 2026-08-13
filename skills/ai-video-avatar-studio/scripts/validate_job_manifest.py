#!/usr/bin/env python3
"""Validate a video-avatar job manifest before render delivery or Drive cleanup.

This script is intentionally deterministic and does not call external services.
It checks the minimum fields required to prevent accidental cleanup of source files.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import pathlib
import sys
from typing import Any


TERMINAL_OK = {"quality_passed", "delivered"}
SOURCE_ROLES = {"avatar_source", "image_reference", "temporary_download"}


def load_manifest(path: pathlib.Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise ValueError(f"manifest not found: {path}") from exc
    except json.JSONDecodeError as exc:
        raise ValueError(f"invalid JSON at line {exc.lineno}, column {exc.colno}") from exc
    if not isinstance(value, dict):
        raise ValueError("manifest root must be an object")
    return value


def file_sha256(path: pathlib.Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def validate(manifest: dict[str, Any], *, cleanup: bool) -> list[str]:
    errors: list[str] = []
    required = ("job_id", "status", "inputs", "scenes", "cleanup")
    errors.extend(f"missing field: {key}" for key in required if key not in manifest)

    if not isinstance(manifest.get("job_id"), str) or not manifest.get("job_id"):
        errors.append("job_id must be a non-empty string")
    if not isinstance(manifest.get("inputs"), list):
        errors.append("inputs must be an array")
    if not isinstance(manifest.get("scenes"), list) or not manifest.get("scenes"):
        errors.append("scenes must be a non-empty array")
    if not isinstance(manifest.get("cleanup"), dict):
        errors.append("cleanup must be an object")

    for index, item in enumerate(manifest.get("inputs", [])):
        if not isinstance(item, dict):
            errors.append(f"inputs[{index}] must be an object")
            continue
        for field in ("asset_id", "file_id", "sha256", "role"):
            if not item.get(field):
                errors.append(f"inputs[{index}] missing {field}")
        if item.get("role") in SOURCE_ROLES and not (
            item.get("source_url") or item.get("consent_record")
        ):
            errors.append(
                f"inputs[{index}] source asset requires source_url or consent_record"
            )

    for index, scene in enumerate(manifest.get("scenes", [])):
        if not isinstance(scene, dict):
            errors.append(f"scenes[{index}] must be an object")
            continue
        for field in ("scene_id", "duration_sec"):
            if field not in scene:
                errors.append(f"scenes[{index}] missing {field}")
        if not isinstance(scene.get("duration_sec"), (int, float)) or scene.get("duration_sec", 0) <= 0:
            errors.append(f"scenes[{index}] duration_sec must be greater than zero")

    cleanup_info = manifest.get("cleanup", {})
    if not isinstance(cleanup_info.get("candidate_file_ids", []), list):
        errors.append("cleanup.candidate_file_ids must be an array")
    if cleanup:
        if manifest.get("status") not in TERMINAL_OK:
            errors.append("cleanup requires status quality_passed or delivered")
        if not manifest.get("outputs"):
            errors.append("cleanup requires at least one verified output")
        quality = manifest.get("quality_gate", {})
        if isinstance(quality, dict) and quality.get("result") not in {"pass", "pass_with_warnings"}:
            errors.append("cleanup requires quality_gate.result pass or pass_with_warnings")
        if cleanup_info.get("trash_allowed") is not True:
            errors.append("cleanup.trash_allowed must be true after explicit authorization")
        if cleanup_info.get("cleanup_done") is True:
            errors.append("cleanup already marked done; use an idempotent status check instead")

        candidate_ids = set(cleanup_info.get("candidate_file_ids", []))
        input_ids = {
            item.get("file_id")
            for item in manifest.get("inputs", [])
            if isinstance(item, dict) and item.get("role") in SOURCE_ROLES
        }
        unknown = sorted(candidate_ids - input_ids)
        if unknown:
            errors.append("cleanup candidates not present as source inputs: " + ", ".join(unknown))

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", type=pathlib.Path)
    parser.add_argument("--cleanup", action="store_true", help="validate preconditions for trashing source files")
    parser.add_argument("--check-file", action="append", type=pathlib.Path, default=[], help="optional local file to print SHA-256 for")
    args = parser.parse_args()

    try:
        manifest = load_manifest(args.manifest)
    except ValueError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    errors = validate(manifest, cleanup=args.cleanup)
    for path in args.check_file:
        if not path.is_file():
            print(f"ERROR: check file not found: {path}", file=sys.stderr)
            errors.append(f"check file not found: {path}")
        else:
            print(json.dumps({"file": str(path), "sha256": file_sha256(path)}, ensure_ascii=False))

    if errors:
        print(json.dumps({"valid": False, "errors": errors}, ensure_ascii=False, indent=2))
        return 1
    print(json.dumps({"valid": True, "cleanup_check": args.cleanup, "job_id": manifest.get("job_id")}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
