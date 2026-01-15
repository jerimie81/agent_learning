# Event Replay Tooling

Purpose: Enable deterministic reconstruction of system state.

## 1. Replay Guarantees

- Deterministic
- Order-preserving
- Side-effect free
- Idempotent

## 2. Replay Modes

### 2.1 Full Replay

```bash
replay --from genesis --to latest
```

### 2.2 Checkpoint Replay

```bash
replay --from checkpoint_id
```

### 2.3 Domain-Scoped Replay

```bash
replay --event-type ConversationRecorded
```

## 3. Replay Engine Responsibilities

- Validate schema per event.
- Verify hash integrity.
- Enforce ordering.
- Feed events to projection builders.

## 4. Replay Failure Handling

| Failure          | Action           |
| ---------------- | ---------------- |
| Hash mismatch    | Abort and alert  |
| Schema violation | Abort            |
| Projection error | Reset projection |

## 5. Audit Mode

Replay engine supports:
- Dry-run mode
- Differential comparison
- Projection diff output
