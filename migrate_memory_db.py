#!/usr/bin/env python3

"""Migrate legacy memory.db contents into an append-only event log."""

from __future__ import annotations

import argparse
import hashlib
import json
import sqlite3
import sys
import uuid
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable


@dataclass(frozen=True)
class EventEnvelope:
    event_id: str
    event_type: str
    timestamp: str
    actor: dict[str, str]
    payload: dict[str, Any]
    schema_version: str
    hash: str


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _canonical_json(value: dict[str, Any]) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def _hash_event(payload: dict[str, Any], metadata: dict[str, Any]) -> str:
    canonical = _canonical_json({"payload": payload, "metadata": metadata})
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def _event_envelope(
    *,
    event_type: str,
    payload: dict[str, Any],
    actor: dict[str, str],
    schema_version: str,
    timestamp: str | None,
) -> EventEnvelope:
    event_id = str(uuid.uuid4())
    ts = timestamp or _utc_now_iso()
    metadata = {
        "event_id": event_id,
        "event_type": event_type,
        "timestamp": ts,
        "actor": actor,
        "schema_version": schema_version,
    }
    event_hash = _hash_event(payload, metadata)
    return EventEnvelope(
        event_id=event_id,
        event_type=event_type,
        timestamp=ts,
        actor=actor,
        payload=payload,
        schema_version=schema_version,
        hash=event_hash,
    )


def _table_names(conn: sqlite3.Connection) -> list[str]:
    rows = conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'"
    ).fetchall()
    return [row[0] for row in rows]


def _table_schema(conn: sqlite3.Connection, table: str) -> dict[str, Any]:
    columns = conn.execute(f"PRAGMA table_info({table})").fetchall()
    foreign_keys = conn.execute(f"PRAGMA foreign_key_list({table})").fetchall()
    return {
        "table": table,
        "columns": [
            {
                "cid": col[0],
                "name": col[1],
                "type": col[2],
                "notnull": bool(col[3]),
                "default": col[4],
                "pk": bool(col[5]),
            }
            for col in columns
        ],
        "foreign_keys": [
            {
                "id": fk[0],
                "seq": fk[1],
                "table": fk[2],
                "from": fk[3],
                "to": fk[4],
                "on_update": fk[5],
                "on_delete": fk[6],
                "match": fk[7],
            }
            for fk in foreign_keys
        ],
    }


def _row_count(conn: sqlite3.Connection, table: str) -> int:
    row = conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()
    return int(row[0]) if row else 0


def _safe_json_loads(value: str) -> Any:
    try:
        return json.loads(value)
    except json.JSONDecodeError:
        return value


def _infer_canonical_event(table: str, row: dict[str, Any]) -> dict[str, Any] | None:
    section = str(row.get("section", "")).strip().lower()
    key = str(row.get("key", "")).strip()
    value = row.get("value")

    if table == "memories" and "user preferences" in section:
        return {
            "event_type": "UserPolicyUpdated",
            "payload": {
                "policy_id": str(uuid.uuid4()),
                "policy_name": key or "legacy_preference",
                "policy_value": _safe_json_loads(value) if value is not None else None,
                "scope": "global",
            },
        }

    if table == "memories":
        content = value if value is not None else ""
        content_hash = hashlib.sha256(str(content).encode("utf-8")).hexdigest()
        return {
            "event_type": "KnowledgeArtifactRegistered",
            "payload": {
                "artifact_id": str(uuid.uuid4()),
                "name": f"{row.get('section', 'legacy')}:{key}".strip(":"),
                "content_hash": content_hash,
                "tags": [row.get("section", "legacy")],
                "source": "import",
            },
        }

    return None


def _iter_rows(conn: sqlite3.Connection, table: str) -> Iterable[dict[str, Any]]:
    conn.row_factory = sqlite3.Row
    cursor = conn.execute(f"SELECT * FROM {table}")
    for row in cursor:
        yield dict(row)


def migrate(
    *,
    db_path: Path,
    events_path: Path,
    schema_path: Path,
    counts_path: Path,
    actor_id: str,
    schema_version: str,
    dry_run: bool,
) -> None:
    if not db_path.exists():
        raise FileNotFoundError(f"Database not found: {db_path}")

    conn = sqlite3.connect(str(db_path))
    try:
        tables = _table_names(conn)
        schema_report = [_table_schema(conn, table) for table in tables]
        counts_report = {table: _row_count(conn, table) for table in tables}

        if not dry_run:
            schema_path.write_text(json.dumps(schema_report, indent=2), encoding="utf-8")
            counts_path.write_text(json.dumps(counts_report, indent=2), encoding="utf-8")

        actor = {"type": "system", "id": actor_id}
        events: list[EventEnvelope] = []

        for table in tables:
            for row in _iter_rows(conn, table):
                canonical = _infer_canonical_event(table, row)
                payload = {
                    "legacy_table": table,
                    "legacy_row": row,
                    "canonical_event": canonical,
                }
                timestamp = row.get("timestamp")
                event = _event_envelope(
                    event_type="LegacyMemoryImported",
                    payload=payload,
                    actor=actor,
                    schema_version=schema_version,
                    timestamp=timestamp,
                )
                events.append(event)

        if dry_run:
            print("Dry run complete.")
            print(json.dumps({"tables": tables, "counts": counts_report}, indent=2))
            return

        with events_path.open("w", encoding="utf-8") as handle:
            for event in events:
                handle.write(_canonical_json(event.__dict__))
                handle.write("\n")

        print("Migration complete.")
        print(f"Events written: {events_path}")
        print(f"Schema report: {schema_path}")
        print(f"Counts report: {counts_path}")
    finally:
        conn.close()


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Migrate legacy memory.db to append-only event log."
    )
    parser.add_argument("--db", type=Path, required=True, help="Path to memory.db")
    parser.add_argument(
        "--events-out",
        type=Path,
        default=Path("events.jsonl"),
        help="Output JSONL event log",
    )
    parser.add_argument(
        "--schema-out",
        type=Path,
        default=Path("schema_report.json"),
        help="Output schema report JSON",
    )
    parser.add_argument(
        "--counts-out",
        type=Path,
        default=Path("row_counts.json"),
        help="Output row counts JSON",
    )
    parser.add_argument(
        "--actor-id",
        type=str,
        default="legacy-migration",
        help="Actor ID for event envelope",
    )
    parser.add_argument(
        "--schema-version",
        type=str,
        default="v1-legacy-migration",
        help="Schema version to record in events",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Audit only; do not write outputs",
    )
    return parser.parse_args(argv)


def main() -> int:
    args = parse_args(sys.argv[1:])
    try:
        migrate(
            db_path=args.db,
            events_path=args.events_out,
            schema_path=args.schema_out,
            counts_path=args.counts_out,
            actor_id=args.actor_id,
            schema_version=args.schema_version,
            dry_run=args.dry_run,
        )
    except Exception as exc:  # noqa: BLE001
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
    