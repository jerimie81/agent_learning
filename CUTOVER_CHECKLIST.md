# Cutover Checklist

Purpose: Ensure a safe, auditable, and reversible transition from legacy stateful memory to a stateless, event-sourced system.

## 1. Pre-Cutover Preconditions (Hard Gates)

### 1.1 Architecture Gates
- [ ] Agent has zero direct access to databases, filesystems, or KV stores.
- [ ] All agent outputs are events only.
- [ ] All agent inputs are explicitly injected.
- [ ] Memory Gateway is the only persistence interface.

### 1.2 Data Gates
- [ ] All legacy memory domains mapped to canonical event types.
- [ ] Event schemas finalized and versioned (v1).
- [ ] Legacy memory.db schema frozen.
- [ ] Snapshot export mechanism validated.

### 1.3 Security Gates
- [ ] Event log is append-only at the storage layer.
- [ ] Hashing enabled for every event.
- [ ] Write authentication enforced.
- [ ] Replay integrity verification implemented.

## 2. Shadow Mode Validation

### 2.1 Dual-Write Verification
- [ ] Every legacy write produces an equivalent event.
- [ ] Event payloads are schema-valid.
- [ ] Event timestamps are monotonic.
- [ ] Event hashes are deterministic.

### 2.2 Read Parity
- [ ] Legacy read results equal projection results.
- [ ] Context windows match exactly.
- [ ] Knowledge retrieval parity verified.
- [ ] Policy decisions identical.

### 2.3 Replay Validation
- [ ] Full replay from genesis succeeds.
- [ ] Partial replay from checkpoint succeeds.
- [ ] Replay produces identical projections.
- [ ] Replay time within acceptable bounds.

## 3. Performance and Stability Gates
- [ ] Event write latency within SLA.
- [ ] Projection rebuild time measured.
- [ ] Gateway throughput load-tested.
- [ ] Failure scenarios simulated (gateway down, projection loss).

## 4. Final Cutover Steps

### 4.1 Freeze Legacy
- [ ] Disable writes to memory.db.
- [ ] Mark database read-only at filesystem level.
- [ ] Export final snapshot.
- [ ] Hash and archive snapshot.

### 4.2 Activate New Path
- [ ] Disable legacy reads.
- [ ] Enable projection-only reads.
- [ ] Monitor gateway error rates.
- [ ] Monitor projection lag.

## 5. Post-Cutover Verification
- [ ] Agent operates without legacy DB present.
- [ ] Projections rebuild successfully from events.
- [ ] No state loss detected.
- [ ] Security monitoring active.

## 6. Rollback Criteria (Emergency Only)

Rollback is permitted only if:
- [ ] Event corruption detected.
- [ ] Replay produces inconsistent state.
- [ ] Gateway policy failure causes data loss.

Rollback steps:
1. Disable gateway writes.
2. Re-enable legacy DB (read/write).
3. Restore snapshot.
4. Document incident.
