# TODO

Project: Stateless Core + Externalized Memory (Option 3a)
Status: Pre-Migration -> Active Refactor
Priority Model: Critical | High | Medium | Low

## 1. Governance and Ground Rules (Critical)
- Formalize stateless agent contract (no implicit memory, no direct storage I/O).
- Declare SQLite forbidden for new memory writes.
- Lock legacy `memory.db` schema as read-only.
- Establish append-only rule for future memory writes.

## 2. Memory Inventory and Decomposition (Critical)
- Extract schema and row counts from legacy `memory.db`.
- Categorize tables into event domains.
- Identify mixed-concern tables.
- Flag non-deterministic or lossy fields.

## 3. Event Store Foundation (Critical)
- Select event transport (Kafka/Redpanda/JetStream).
- Select warm persistence layer (PostgreSQL JSONB or equivalent).
- Define cold archive strategy (WORM object storage).
- Implement hashing, monotonic ordering, and immutability.

## 4. Memory Gateway Service (Critical)
- Design and implement gateway API.
- Enforce policy checks and auth at the boundary.
- Block agent access to raw storage backends.
- Add audit logging for every request.

## 5. Read-Side Projections (Critical)
- Implement projection services (context, knowledge, tooling, policy).
- Build deterministic replay and rebuild utilities.
- Validate replay correctness and measure rebuild time.

## 6. Agent Core Refactor (Critical)
- Remove direct DB access from agent code.
- Require explicit context injection per request.
- Validate pure-function behavior with tests.

## 7. Dual-Write Migration Phase (Critical)
- Enable dual-write (legacy DB + event log).
- Compare legacy reads to projections; resolve drift.
- Pass replay determinism and performance benchmarks.

## 8. Legacy Decommissioning (Critical)
- Freeze legacy DB, export snapshot, and convert to events.
- Verify replay from snapshot produces identical state.
- Archive legacy DB and remove write permissions.

## 9. Security and Threat Modeling (High)
- Complete threat modeling and hardening.
- Add anomaly detection and integrity verification.
- Define key rotation plan.

## 10. Documentation and Operations (High)
- Ensure all architecture and ops docs are current.
- Add local dev bootstrap scripts and fixtures.

## 11. Post-Migration Enhancements (Medium)
- Multi-agent isolation via per-stream namespaces.
- Cross-model shared memory via event federation.
- Offline replay sandbox and forensic timeline visualizer.

## 12. Exit Criteria
- Agent is stateless.
- All memory is externalized and event-sourced.
- Legacy storage fully decommissioned.
- Full state reconstructed from events alone.
- Security audit passes with no critical findings.

## Supporting Artifacts
- `CUTOVER_CHECKLIST.md`
- `EVENT_SCHEMAS_v1.md`
- `MEMORY_GATEWAY_API.md`
- `THREAT_MODEL.md`
- `PROJECTION_DESIGN.md`
- `EVENT_REPLAY_TOOLING.md`
- `SECURITY_AUDIT_CHECKLIST.md`
- `OPERATOR_RUNBOOK.md`
