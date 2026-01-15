# agent_learning

Stateless Core + Externalized Memory Services (Event-Sourced, Multi-Backend) for a hardened, security-first, multi-agent LLM system.

## Migration Tooling

`migrate_memory_db.py` exports a legacy SQLite `memory.db` into an append-only JSONL event log and emits schema + row-count reports.

Dry-run audit:

```bash
python3 migrate_memory_db.py --db /path/to/memory.db --dry-run
```

Write outputs:

```bash
python3 migrate_memory_db.py \
  --db /path/to/memory.db \
  --events-out events.jsonl \
  --schema-out schema_report.json \
  --counts-out row_counts.json
```

## Documentation

- `TODO.md`
- `CUTOVER_CHECKLIST.md`
- `EVENT_SCHEMAS_v1.md`
- `MEMORY_GATEWAY_API.md`
- `THREAT_MODEL.md`
- `PROJECTION_DESIGN.md`
- `EVENT_REPLAY_TOOLING.md`
- `SECURITY_AUDIT_CHECKLIST.md`
- `OPERATOR_RUNBOOK.md`
