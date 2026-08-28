#!/usr/bin/env python3
"""
@file scripts/record_activity.py
@project 123panSkill
@module Private skill activity recorder
@description Appends and validates de-identified JSONL outcome records for 123pan skill workflows.
@logic Restricts event fields to controlled values, appends records to a local owner-readable log, and validates existing JSONL entries before display.
@dependencies Python standard library only.
@index_tags 123pan, activity-log, jsonl, privacy, audit
@author holic512
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable


DEFAULT_LOG_FILE = Path(".123pan-skill") / "activity.jsonl"
EVENT_NAME = "123pan-skill-activity"
SCHEMA_VERSION = 1
SAFE_LABEL = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
SOURCE_SNAPSHOT = re.compile(
    r"^(?:archive-baseline|working-copy|external-runtime|upstream-history-[a-z0-9][a-z0-9._-]{0,80})$"
)
ALLOWED_ACTIONS = {
    "client-inspection",
    "remote-read",
    "remote-mutation",
    "upstream-review",
    "archive-refresh",
    "skill-maintenance",
}
ALLOWED_OUTCOMES = {"started", "succeeded", "failed", "skipped"}
ALLOWED_SIDE_EFFECTS = {"none", "local-write", "remote-read", "remote-write", "mixed"}
ALLOWED_AUTHORIZATION = {"not-applicable", "confirmed", "not-confirmed"}
REQUIRED_KEYS = {
    "event",
    "schema_version",
    "timestamp",
    "run_id",
    "action",
    "outcome",
    "side_effect",
    "authorization",
    "source_snapshot",
    "reason_code",
    "validations",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Append or inspect de-identified local 123pan skill activity records."
    )
    parser.add_argument(
        "--log-file",
        type=Path,
        default=DEFAULT_LOG_FILE,
        help="Local JSONL file; default: .123pan-skill/activity.jsonl in the current directory.",
    )
    subcommands = parser.add_subparsers(dest="command", required=True)

    record = subcommands.add_parser("record", help="Append one validated outcome record.")
    record.add_argument("--action", choices=sorted(ALLOWED_ACTIONS), required=True)
    record.add_argument("--outcome", choices=sorted(ALLOWED_OUTCOMES), required=True)
    record.add_argument("--side-effect", choices=sorted(ALLOWED_SIDE_EFFECTS), required=True)
    record.add_argument(
        "--authorization", choices=sorted(ALLOWED_AUTHORIZATION), required=True
    )
    record.add_argument("--source-snapshot", required=True)
    record.add_argument("--reason-code", required=True)
    record.add_argument("--validation", action="append", default=[])
    record.add_argument("--run-id", type=uuid.UUID)
    record.add_argument("--dry-run", action="store_true")

    subcommands.add_parser("location", help="Print the resolved local log path.")
    subcommands.add_parser("list", help="Print validated JSONL records.")
    subcommands.add_parser("validate", help="Validate JSONL records without printing them.")
    return parser.parse_args()


def utc_timestamp() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def validate_label(value: str, field: str) -> str:
    if not SAFE_LABEL.fullmatch(value) or len(value) > 80:
        raise ValueError(f"{field} must be a lowercase hyphen-separated label of at most 80 characters")
    return value


def validate_source_snapshot(value: str) -> str:
    if not SOURCE_SNAPSHOT.fullmatch(value):
        raise ValueError(
            "source_snapshot must be archive-baseline, working-copy, external-runtime, "
            "or upstream-history-<safe-id>"
        )
    return value


def validate_timestamp(value: Any) -> str:
    if not isinstance(value, str) or not value.endswith("Z"):
        raise ValueError("timestamp must be an ISO-8601 UTC string ending in Z")
    try:
        datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as error:
        raise ValueError("timestamp must be a valid ISO-8601 UTC string") from error
    return value


def validate_record(record: Any) -> dict[str, Any]:
    if not isinstance(record, dict) or set(record) != REQUIRED_KEYS:
        raise ValueError("record must contain exactly the supported de-identified schema fields")
    if record["event"] != EVENT_NAME or record["schema_version"] != SCHEMA_VERSION:
        raise ValueError("unsupported event name or schema version")
    validate_timestamp(record["timestamp"])
    try:
        uuid.UUID(record["run_id"])
    except (AttributeError, ValueError, TypeError) as error:
        raise ValueError("run_id must be a UUID") from error
    if record["action"] not in ALLOWED_ACTIONS:
        raise ValueError("unsupported action")
    if record["outcome"] not in ALLOWED_OUTCOMES:
        raise ValueError("unsupported outcome")
    if record["side_effect"] not in ALLOWED_SIDE_EFFECTS:
        raise ValueError("unsupported side_effect")
    if record["authorization"] not in ALLOWED_AUTHORIZATION:
        raise ValueError("unsupported authorization")
    validate_source_snapshot(record["source_snapshot"])
    validate_label(record["reason_code"], "reason_code")
    if not isinstance(record["validations"], list):
        raise ValueError("validations must be a list")
    for validation in record["validations"]:
        validate_label(validation, "validation")
    return record


def build_record(args: argparse.Namespace) -> dict[str, Any]:
    return validate_record(
        {
            "event": EVENT_NAME,
            "schema_version": SCHEMA_VERSION,
            "timestamp": utc_timestamp(),
            "run_id": str(args.run_id or uuid.uuid4()),
            "action": args.action,
            "outcome": args.outcome,
            "side_effect": args.side_effect,
            "authorization": args.authorization,
            "source_snapshot": args.source_snapshot,
            "reason_code": args.reason_code,
            "validations": args.validation,
        }
    )


def ensure_parent_directory(log_file: Path) -> None:
    if not log_file.parent.exists():
        log_file.parent.mkdir(mode=0o700, parents=True, exist_ok=False)


def append_record(log_file: Path, record: dict[str, Any]) -> None:
    ensure_parent_directory(log_file)
    flags = os.O_WRONLY | os.O_APPEND | os.O_CREAT
    descriptor = os.open(log_file, flags, 0o600)
    payload = json.dumps(record, ensure_ascii=False, separators=(",", ":")) + "\n"
    with os.fdopen(descriptor, "a", encoding="utf-8") as handle:
        try:
            import fcntl

            fcntl.flock(handle.fileno(), fcntl.LOCK_EX)
        except ImportError:
            pass
        try:
            handle.write(payload)
            handle.flush()
            os.fsync(handle.fileno())
        finally:
            try:
                import fcntl

                fcntl.flock(handle.fileno(), fcntl.LOCK_UN)
            except ImportError:
                pass


def iter_records(log_file: Path) -> Iterable[dict[str, Any]]:
    if not log_file.exists():
        return []
    records: list[dict[str, Any]] = []
    with log_file.open("r", encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, start=1):
            if not line.strip():
                raise ValueError(f"line {line_number}: blank lines are not allowed")
            try:
                record = json.loads(line)
            except json.JSONDecodeError as error:
                raise ValueError(f"line {line_number}: invalid JSON") from error
            try:
                records.append(validate_record(record))
            except ValueError as error:
                raise ValueError(f"line {line_number}: {error}") from error
    return records


def main() -> int:
    args = parse_args()
    log_file = args.log_file.expanduser().resolve()
    try:
        if args.command == "location":
            print(log_file)
            return 0
        if args.command == "record":
            record = build_record(args)
            if args.dry_run:
                print(json.dumps(record, ensure_ascii=False, indent=2))
                return 0
            append_record(log_file, record)
            print(json.dumps({"recorded": True, "log_file": str(log_file), "run_id": record["run_id"]}))
            return 0
        records = list(iter_records(log_file))
        if args.command == "list":
            for record in records:
                print(json.dumps(record, ensure_ascii=False, separators=(",", ":")))
        print(json.dumps({"valid": True, "record_count": len(records), "log_file": str(log_file)}))
        return 0
    except (OSError, ValueError) as error:
        print(f"activity log error: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
