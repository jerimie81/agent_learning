#!/usr/bin/env python3

from __future__ import annotations

import argparse
import hashlib
import json
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


REQUIRED_FIELDS = {
    "event_id",
    "event_type",
    "timestamp",
    "actor",
    "payload",
    "schema_version",
    "hash",
}


def _canonical_json(value: dict[str, Any]) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def _parse_timestamp(value: str) -> bool:
    text = value.strip()
    if text.endswith("Z"):
        text = f"{text[:-1]}+00:00"
    try:
        parsed = datetime.fromisoformat(text)
    except ValueError:
        return False
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.tzinfo is not None


def _validate_uuid_v7(value: str) -> bool:
    try:
        parsed = uuid.UUID(value)
    except ValueError:
        return False
    return parsed.version == 7


def _compute_hash(event: dict[str, Any]) -> str:
    metadata = {
        "event_id": event["event_id"],
        "event_type": event["event_type"],
        "timestamp": event["timestamp"],
        "actor": event["actor"],
        "schema_version": event["schema_version"],
    }
    canonical = _canonical_json({"payload": event["payload"], "metadata": metadata})
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def validate_file(path: Path) -> list[str]:
    issues: list[str] = []
    for line_no, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        try:
            event = json.loads(line)
        except json.JSONDecodeError as exc:
            issues.append(f"line {line_no}: invalid JSON: {exc}")
            continue
        missing = REQUIRED_FIELDS - event.keys()
        if missing:
            issues.append(f"line {line_no}: missing fields: {sorted(missing)}")
            continue
        actor = event.get("actor")
        if not isinstance(actor, dict) or "type" not in actor or "id" not in actor:
            issues.append(f"line {line_no}: actor must include type and id")
        if not _parse_timestamp(str(event.get("timestamp", ""))):
            issues.append(f"line {line_no}: timestamp must be ISO-8601 with tz")
        if not _validate_uuid_v7(str(event.get("event_id", ""))):
            issues.append(f"line {line_no}: event_id must be uuid-v7")
        expected_hash = _compute_hash(event)
        if event.get("hash") != expected_hash:
            issues.append(f"line {line_no}: hash mismatch")
    return issues


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate event log JSONL.")
    parser.add_argument("--events", type=Path, required=True, help="Path to events.jsonl")
    parser.add_argument(
        "--allow-missing",
        action="store_true",
        help="Exit successfully if the file does not exist.",
    )
    return parser.parse_args(argv)


def main() -> int:
    args = parse_args(sys.argv[1:])
    if not args.events.exists():
        if args.allow_missing:
            print(f"events file not found, skipping: {args.events}")
            return 0
        print(f"events file not found: {args.events}", file=sys.stderr)
        return 1
    issues = validate_file(args.events)
    if issues:
        print("Validation issues:")
        for issue in issues:
            print(f"- {issue}")
        return 1
    print("Validation OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
