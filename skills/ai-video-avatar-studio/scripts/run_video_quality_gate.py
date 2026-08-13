#!/usr/bin/env python3
"""Run deterministic video quality gates and safely quarantine local temp files.

The script never deletes files by default.  Use --cleanup to move only manifest-listed
local candidates into a timestamped .cleanup-trash directory after all required gates
pass. Permanent deletion requires two explicit flags and is intentionally discouraged.
"""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import math
import os
import pathlib
import re
import shutil
import subprocess
import sys
from typing import Any

VERSION = "1.0.0"
PASS_RESULTS = {"pass", "pass_with_warnings"}
PROTECTED_DIRS = {"sources", "source", "originals", "original", "final", "deliverables", "delivery"}
PROTECTED_NAMES = {"manifest.json", "quality-report.json", "quality_report.json", "cleanup-log.json"}


def now_utc() -> str:
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def load_json(path: pathlib.Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: pathlib.Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def sha256_file(path: pathlib.Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def run_command(command: list[str]) -> tuple[int, str, str]:
    try:
        completed = subprocess.run(command, capture_output=True, text=True, check=False)
    except FileNotFoundError as exc:
        return 127, "", str(exc)
    return completed.returncode, completed.stdout, completed.stderr


def add_check(checks: list[dict[str, Any]], name: str, status: str, message: str, **details: Any) -> None:
    checks.append({"name": name, "status": status, "message": message, "details": details})


def parse_number(value: Any) -> float | None:
    try:
        if value is None or value == "N/A":
            return None
        return float(value)
    except (TypeError, ValueError):
        return None


def parse_ratio(value: Any) -> float | None:
    if value is None:
        return None
    text = str(value).strip()
    if ":" in text:
        left, right = text.split(":", 1)
        try:
            return float(left) / float(right)
        except (ValueError, ZeroDivisionError):
            return None
    return parse_number(text)


def media_duration(probe: dict[str, Any], stream_type: str | None = None) -> float | None:
    if stream_type:
        for stream in probe.get("streams", []):
            if stream.get("codec_type") == stream_type:
                duration = parse_number(stream.get("duration"))
                if duration is not None:
                    return duration
    return parse_number(probe.get("format", {}).get("duration"))


def locate_video(manifest: dict[str, Any], manifest_path: pathlib.Path, override: str | None) -> pathlib.Path | None:
    candidates: list[str] = []
    if override:
        candidates.append(override)
    if isinstance(manifest.get("final_video"), str):
        candidates.append(manifest["final_video"])
    outputs = manifest.get("outputs", [])
    if isinstance(outputs, list):
        for output in outputs:
            if isinstance(output, str):
                candidates.append(output)
            elif isinstance(output, dict):
                for key in ("local_path", "path", "file"):
                    if isinstance(output.get(key), str):
                        candidates.append(output[key])
    for raw in candidates:
        path = pathlib.Path(raw).expanduser()
        if not path.is_absolute():
            path = manifest_path.parent / path
        if path.exists():
            return path.resolve()
    if candidates:
        path = pathlib.Path(candidates[0]).expanduser()
        if not path.is_absolute():
            path = manifest_path.parent / path
        return path.resolve()
    return None


def expected_settings(manifest: dict[str, Any]) -> dict[str, Any]:
    settings = manifest.get("quality_requirements")
    return settings if isinstance(settings, dict) else {}


def inspect_captions(path: pathlib.Path, duration: float | None) -> tuple[list[tuple[float, float]], list[str]]:
    errors: list[str] = []
    intervals: list[tuple[float, float]] = []
    try:
        text = path.read_text(encoding="utf-8-sig")
    except OSError as exc:
        return [], [f"cannot read captions: {exc}"]
    if path.suffix.lower() == ".json":
        try:
            value = json.loads(text)
        except json.JSONDecodeError as exc:
            return [], [f"invalid captions JSON: {exc}"]
        if isinstance(value, dict):
            value = value.get("captions", value.get("segments", []))
        if not isinstance(value, list):
            return [], ["captions JSON must be an array or contain captions/segments"]
        for index, item in enumerate(value):
            if not isinstance(item, dict):
                errors.append(f"caption[{index}] must be an object")
                continue
            start = parse_number(item.get("start", item.get("start_sec")))
            end = parse_number(item.get("end", item.get("end_sec")))
            if start is None or end is None:
                errors.append(f"caption[{index}] needs numeric start and end")
            else:
                intervals.append((start, end))
    else:
        blocks = re.split(r"\n\s*\n", text.strip()) if text.strip() else []
        pattern = re.compile(r"(\d{1,2}):(\d{2}):(\d{2})[,\.](\d{3})\s+-->\s+(\d{1,2}):(\d{2}):(\d{2})[,\.](\d{3})")
        for index, block in enumerate(blocks):
            match = pattern.search(block)
            if not match:
                errors.append(f"caption block {index + 1} has invalid timestamp")
                continue
            values = [int(value) for value in match.groups()]
            start = values[0] * 3600 + values[1] * 60 + values[2] + values[3] / 1000
            end = values[4] * 3600 + values[5] * 60 + values[6] + values[7] / 1000
            intervals.append((start, end))
    previous_end = -math.inf
    for index, (start, end) in enumerate(intervals):
        if start < 0 or end <= start:
            errors.append(f"caption[{index}] has invalid interval {start}..{end}")
        if duration is not None and end > duration + 0.05:
            errors.append(f"caption[{index}] ends after video duration")
        if start < previous_end - 0.02:
            errors.append(f"caption[{index}] overlaps the previous caption")
        previous_end = max(previous_end, end)
    return intervals, errors


def get_cleanup_candidates(manifest: dict[str, Any]) -> list[str]:
    cleanup = manifest.get("cleanup", {})
    if not isinstance(cleanup, dict):
        return []
    values = cleanup.get("local_candidate_paths", cleanup.get("local_candidates", []))
    if not isinstance(values, list):
        return []
    return [str(value) for value in values if isinstance(value, (str, pathlib.Path))]


def is_within(path: pathlib.Path, root: pathlib.Path) -> bool:
    try:
        path.relative_to(root)
        return True
    except ValueError:
        return False


def cleanup_candidates(
    manifest: dict[str, Any],
    manifest_path: pathlib.Path,
    report_path: pathlib.Path,
    *,
    allowed: bool,
    cleanup_requested: bool,
    permanent: bool,
    confirm_permanent: bool,
) -> dict[str, Any]:
    cleanup = manifest.get("cleanup", {})
    root_raw = cleanup.get("job_root") if isinstance(cleanup, dict) else None
    root = pathlib.Path(root_raw).expanduser() if isinstance(root_raw, str) else manifest_path.parent
    if not root.is_absolute():
        root = manifest_path.parent / root
    root = root.resolve()
    quarantine_root = root / ".cleanup-trash" / dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    actions: list[dict[str, Any]] = []
    if not cleanup_requested:
        mode = "dry-run"
    elif permanent and not confirm_permanent:
        mode = "blocked-permanent-delete-confirmation-missing"
    elif not allowed:
        mode = "blocked-quality-gate"
    elif permanent:
        mode = "permanent-delete"
    else:
        mode = "quarantine"

    protected = {manifest_path.resolve(), report_path.resolve()}
    final_video = locate_video(manifest, manifest_path, None)
    if final_video:
        protected.add(final_video)
    for raw in get_cleanup_candidates(manifest):
        candidate = pathlib.Path(raw).expanduser()
        if not candidate.is_absolute():
            candidate = root / candidate
        resolved = candidate.resolve(strict=False)
        record: dict[str, Any] = {"path": str(candidate), "resolved_path": str(resolved), "action": "blocked"}
        if not is_within(resolved, root) or resolved == root:
            record["reason"] = "candidate is outside job_root or is job_root"
        elif resolved in protected:
            record["reason"] = "protected manifest, report, final video, or output"
        elif any(part.lower() in PROTECTED_DIRS for part in resolved.relative_to(root).parts[:-1]):
            record["reason"] = "candidate is inside a protected directory"
        elif resolved.name in PROTECTED_NAMES or resolved.name.startswith("."):
            record["reason"] = "protected filename"
        elif candidate.is_symlink() or resolved.is_symlink():
            record["reason"] = "symlink candidates are never cleaned automatically"
        elif not candidate.exists():
            record["action"] = "already_absent"
            record["reason"] = "candidate does not exist"
        elif not candidate.is_file():
            record["reason"] = "candidate is not a regular file"
        elif mode == "blocked-quality-gate":
            record["reason"] = "quality gate did not authorize cleanup"
        elif mode == "blocked-permanent-delete-confirmation-missing":
            record["reason"] = "permanent delete requires --confirm-permanent-delete"
        elif mode == "dry-run":
            record["action"] = "would_quarantine"
        else:
            try:
                if mode == "permanent-delete":
                    candidate.unlink()
                    record["action"] = "permanently_deleted"
                else:
                    destination = quarantine_root / resolved.relative_to(root)
                    destination.parent.mkdir(parents=True, exist_ok=True)
                    if destination.exists():
                        record["action"] = "already_quarantined"
                        record["destination"] = str(destination)
                    else:
                        shutil.move(str(candidate), str(destination))
                        record["action"] = "quarantined"
                        record["destination"] = str(destination)
            except OSError as exc:
                record["reason"] = f"cleanup failed: {exc}"
        actions.append(record)
    return {"mode": mode, "job_root": str(root), "quarantine_root": str(quarantine_root), "actions": actions}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", type=pathlib.Path)
    parser.add_argument("--video", help="override the final video path from the manifest")
    parser.add_argument("--report-out", type=pathlib.Path, help="quality report path")
    parser.add_argument("--cleanup", action="store_true", help="quarantine allowlisted local candidates after a passing gate")
    parser.add_argument("--allow-warnings", action="store_true", help="allow pass_with_warnings to authorize cleanup")
    parser.add_argument("--permanent-delete", action="store_true", help="permanently delete candidates instead of quarantining")
    parser.add_argument("--confirm-permanent-delete", action="store_true", help="required together with --permanent-delete")
    parser.add_argument("--skip-decode-check", action="store_true", help="skip full ffmpeg decode check")
    args = parser.parse_args()

    manifest_path = args.manifest.expanduser().resolve()
    report_path = (args.report_out or manifest_path.parent / "quality-report.json").expanduser().resolve()
    checks: list[dict[str, Any]] = []
    errors: list[str] = []
    warnings: list[str] = []
    try:
        manifest = load_json(manifest_path)
    except (OSError, json.JSONDecodeError) as exc:
        report = {"version": VERSION, "checked_at": now_utc(), "result": "fail", "errors": [str(exc)], "checks": []}
        write_json(report_path, report)
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return 1
    if not isinstance(manifest, dict):
        errors.append("manifest root must be an object")
        manifest = {}

    video_path = locate_video(manifest, manifest_path, args.video)
    probe: dict[str, Any] = {}
    if not video_path or not video_path.is_file() or video_path.stat().st_size <= 0:
        errors.append("final video is missing or empty")
        add_check(checks, "file_integrity", "fail", "final video is missing or empty")
    else:
        add_check(checks, "file_integrity", "pass", "final video exists and is non-empty", path=str(video_path), size=video_path.stat().st_size)
        code, stdout, stderr = run_command(["ffprobe", "-v", "error", "-print_format", "json", "-show_format", "-show_streams", str(video_path)])
        if code != 0:
            errors.append("ffprobe could not read final video")
            add_check(checks, "ffprobe", "fail", "ffprobe failed", stderr=stderr[-2000:])
        else:
            try:
                probe = json.loads(stdout)
                add_check(checks, "ffprobe", "pass", "ffprobe metadata read successfully")
            except json.JSONDecodeError:
                errors.append("ffprobe returned invalid JSON")
                add_check(checks, "ffprobe", "fail", "ffprobe returned invalid JSON")

    video_streams = [s for s in probe.get("streams", []) if s.get("codec_type") == "video"]
    audio_streams = [s for s in probe.get("streams", []) if s.get("codec_type") == "audio"]
    settings = expected_settings(manifest)
    if video_streams:
        stream = video_streams[0]
        width, height = stream.get("width"), stream.get("height")
        duration = media_duration(probe, "video")
        fps = parse_ratio(stream.get("avg_frame_rate") or stream.get("r_frame_rate"))
        add_check(checks, "video_stream", "pass", "video stream is present", codec=stream.get("codec_name"), width=width, height=height, duration_sec=duration, fps=fps)
        if settings.get("width") is not None and width != settings.get("width"):
            errors.append(f"width mismatch: expected {settings['width']}, got {width}")
        if settings.get("height") is not None and height != settings.get("height"):
            errors.append(f"height mismatch: expected {settings['height']}, got {height}")
        expected_ratio = parse_ratio(settings.get("aspect_ratio"))
        actual_ratio = width / height if width and height else None
        if expected_ratio and actual_ratio and abs(actual_ratio - expected_ratio) > float(settings.get("aspect_ratio_tolerance", 0.02)):
            errors.append(f"aspect ratio mismatch: expected {expected_ratio:.4f}, got {actual_ratio:.4f}")
        expected_duration = parse_number(settings.get("duration_sec", settings.get("target_duration_sec")))
        tolerance = parse_number(settings.get("duration_tolerance_sec")) or 0.35
        if expected_duration is not None and duration is not None and abs(duration - expected_duration) > tolerance:
            errors.append(f"duration mismatch: expected {expected_duration:.3f}s ± {tolerance:.3f}s, got {duration:.3f}s")
        expected_fps = parse_ratio(settings.get("fps"))
        fps_tolerance = parse_number(settings.get("fps_tolerance")) or 0.02
        if expected_fps is not None and fps is not None and abs(fps - expected_fps) > fps_tolerance:
            errors.append(f"fps mismatch: expected {expected_fps:.3f}, got {fps:.3f}")
        add_check(checks, "geometry_timing", "fail" if any("mismatch" in e for e in errors) else "pass", "geometry and timing checked", duration_sec=duration, fps=fps)
    else:
        errors.append("video stream is missing")
        add_check(checks, "video_stream", "fail", "video stream is missing")

    duration = media_duration(probe, "video")
    audio_required = bool(settings.get("audio_required", manifest.get("audio_required", False)))
    if audio_streams:
        audio_duration = media_duration(probe, "audio")
        drift = abs((duration or audio_duration or 0) - (audio_duration or duration or 0))
        add_check(checks, "audio", "pass", "audio stream present", codec=audio_streams[0].get("codec_name"), duration_sec=audio_duration, duration_drift_sec=drift)
        if drift > float(settings.get("av_duration_tolerance_sec", 0.35)):
            errors.append(f"audio/video duration drift is {drift:.3f}s")
    elif audio_required:
        errors.append("audio stream is required but missing")
        add_check(checks, "audio", "fail", "required audio stream is missing")
    else:
        add_check(checks, "audio", "warning", "audio stream is absent but not required")
        warnings.append("audio stream is absent but not required")

    if video_path and video_path.is_file():
        if args.skip_decode_check:
            add_check(checks, "decode", "warning", "full decode check was skipped")
            warnings.append("full decode check was skipped")
        else:
            code, _, stderr = run_command(["ffmpeg", "-v", "error", "-i", str(video_path), "-f", "null", "-"])
            if code != 0:
                errors.append("ffmpeg decode check failed")
                add_check(checks, "decode", "fail", "full decode check failed", stderr=stderr[-2000:])
            else:
                add_check(checks, "decode", "pass", "full decode check passed")

    captions_value = manifest.get("captions_path")
    if isinstance(manifest.get("captions"), dict):
        captions_value = manifest["captions"].get("path", captions_value)
    captions_required = bool(settings.get("captions_required", manifest.get("captions_required", False)))
    if captions_value:
        captions_path = pathlib.Path(str(captions_value)).expanduser()
        if not captions_path.is_absolute():
            captions_path = manifest_path.parent / captions_path
        intervals, caption_errors = inspect_captions(captions_path, duration)
        if caption_errors:
            errors.extend(caption_errors)
            add_check(checks, "captions", "fail", "caption timing validation failed", path=str(captions_path), count=len(intervals), errors=caption_errors)
        else:
            add_check(checks, "captions", "pass", "caption timing validation passed", path=str(captions_path), count=len(intervals))
    elif captions_required:
        errors.append("captions are required but captions path is missing")
        add_check(checks, "captions", "fail", "required captions are missing")
    else:
        add_check(checks, "captions", "warning", "captions are absent but not required")
        warnings.append("captions are absent but not required")

    semantic = manifest.get("semantic_review", {})
    required_semantic = settings.get("required_semantic_gates", [])
    if isinstance(required_semantic, list):
        for gate in required_semantic:
            if not isinstance(gate, str):
                continue
            status = semantic.get(gate) if isinstance(semantic, dict) else None
            if status == "pass":
                add_check(checks, gate, "pass", "required semantic gate passed")
            elif status == "pass_with_warnings":
                add_check(checks, gate, "warning", "semantic gate passed with warnings")
                warnings.append(f"semantic gate warning: {gate}")
            else:
                errors.append(f"required semantic gate not passed: {gate}={status!r}")
                add_check(checks, gate, "fail", "required semantic gate did not pass", gate_status=status)

    provenance = manifest.get("provenance_status")
    if settings.get("provenance_required", False) and provenance != "pass":
        errors.append(f"provenance gate not passed: {provenance!r}")
        add_check(checks, "provenance", "fail", "required provenance gate did not pass", gate_status=provenance)
    else:
        add_check(checks, "provenance", "pass" if provenance == "pass" else "warning", "provenance checked", gate_status=provenance)

    final_hash = sha256_file(video_path) if video_path and video_path.is_file() else None
    if final_hash:
        add_check(checks, "output_hash", "pass", "final output SHA-256 recorded", sha256=final_hash)

    result = "fail" if errors else ("pass_with_warnings" if warnings else "pass")
    allow_warnings = args.allow_warnings or bool(settings.get("allow_warnings", False))
    cleanup_allowed = result == "pass" or (result == "pass_with_warnings" and allow_warnings)
    if args.cleanup and manifest.get("cleanup", {}).get("local_cleanup_allowed") is not True:
        cleanup_allowed = False
        warnings.append("cleanup requested but manifest cleanup.local_cleanup_allowed is not true")
    cleanup_info = cleanup_candidates(
        manifest,
        manifest_path,
        report_path,
        allowed=cleanup_allowed and not errors,
        cleanup_requested=args.cleanup,
        permanent=args.permanent_delete,
        confirm_permanent=args.confirm_permanent_delete,
    )
    if args.cleanup and cleanup_info["mode"].startswith("blocked"):
        errors.append(f"cleanup blocked: {cleanup_info['mode']}")
        result = "fail"

    report = {
        "report_version": VERSION,
        "checked_at": now_utc(),
        "job_id": manifest.get("job_id"),
        "result": result,
        "video": {"path": str(video_path) if video_path else None, "sha256": final_hash, "probe": probe},
        "checks": checks,
        "errors": errors,
        "warnings": warnings,
        "cleanup": cleanup_info,
        "protection": {"never_delete": ["final video", "manifest", "quality report", "source assets", "first/last frames"]},
    }
    write_json(report_path, report)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if result in PASS_RESULTS else 1


if __name__ == "__main__":
    raise SystemExit(main())
