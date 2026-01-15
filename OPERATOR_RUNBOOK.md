# Operator Runbook

Purpose: Guide operators during normal operation, incidents, and recovery.

## 1. Normal Operations

### 1.1 Daily Checks

- Event ingestion rate.
- Projection lag.
- Gateway error rate.

### 1.2 Weekly Checks

- Projection rebuild test.
- Event log integrity scan.
- Cold archive verification.

## 2. Incident Response

### 2.1 Suspected Memory Corruption

1. Freeze event ingestion.
2. Snapshot event log.
3. Replay into clean environment.
4. Compare projections.
5. Resume or rollback.

### 2.2 Gateway Compromise

1. Rotate credentials.
2. Disable writes.
3. Audit recent events.
4. Rebuild projections.
5. Resume with clean state.

## 3. Disaster Recovery

- Event log is primary asset.
- Projections rebuilt from scratch.
- No reliance on backups beyond events.

## 4. Operator Prohibitions

Operators must not:
- Modify events.
- Patch projections manually.
- Restore legacy DB writes.
- Bypass gateway policies.
