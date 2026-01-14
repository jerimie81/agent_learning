:
Below is a release-ready TODO.md aligned to Option 3a: Stateless Core + Externalized, Event-Sourced Memory Services and grounded in the current artifacts, scripts, and migration dossier you are working from.

This is written to be actionable, auditable, and suitable for use as a primary execution checklist during the migration.

TODO.md
Project: Stateless Core + Externalized Memory (Option 3a)
Status: Pre-Migration → Active Refactor
Priority Model: 🔴 Critical | 🟠 High | 🟡 Medium | 🟢 Low

1. Governance & Ground Rules
🔴 Define Non-Negotiables
 Formalize stateless agent contract (no implicit memory, no direct storage I/O)

 Declare SQLite forbidden for any new memory writes

 Lock current memory.db schema as legacy-only

 Establish append-only rule for all future memory writes

🟠 Policy & Compliance
 Define data retention policies per event type

 Define PII / sensitive data classification rules

 Specify cryptographic standards (hashing, signing, verification)

 Document zero-trust assumptions explicitly

2. Memory Inventory & Decomposition
🔴 Legacy Memory Audit
 Extract full schema and row counts from memory.db

 Categorize all tables into event domains

 Identify mixed-concern tables (e.g., conversations + preferences)

 Flag non-deterministic or lossy fields

🟠 Canonical Event Mapping
 Define Event Taxonomy v1

Conversation events

Knowledge artifact events

User policy events

Execution / tooling events

 Create canonical JSON schema for each event type

 Version all schemas explicitly (schema_version)

3. Event Store Foundation
🔴 Event Log Selection
 Select primary event transport (Kafka / Redpanda / JetStream)

 Select warm persistence layer (PostgreSQL JSONB or equivalent)

 Define cold archive strategy (WORM object storage)

🔴 Event Integrity
 Implement SHA-256 (or stronger) event hashing

 Implement monotonic ordering guarantees

 Enforce immutability at storage layer

 Implement write-once permissions

🟠 Tooling
 Build minimal event writer CLI

 Build event replay utility

 Build event validation / schema linter

4. Memory Gateway Service
🔴 Gateway Core
 Design Memory Gateway API (read / write / project)

 Enforce policy checks at gateway boundary

 Block agent access to raw storage backends

 Implement request authentication / authorization

🟠 Routing & Policy
 Route writes → event log only

 Route reads → projections only

 Implement per-event-type rate limiting

 Add audit logging for every request

5. Read-Side Projections
🔴 Projection Services
 Conversation context projection (KV / Redis)

 Knowledge search projection (vector DB)

 Tool / command index projection (SQL)

 Policy cache projection (in-memory)

🟠 Rebuild & Recovery
 Implement full projection rebuild from genesis

 Validate deterministic replay correctness

 Measure rebuild time and memory usage

 Test projection discard + rebuild scenarios

6. Agent Core Refactor
🔴 Stateless Enforcement
 Remove all direct DB access from agent code

 Remove assumptions of prior context

 Require explicit context injection per request

 Block write access except via emitted events

🟠 Interface Contract
 Define strict input payload schema

 Define strict output payload schema

 Validate pure-function behavior (same input → same output)

 Add unit tests for stateless guarantees

7. Dual-Write Migration Phase
🔴 Shadow Mode
 Enable dual-write (legacy DB + event log)

 Compare legacy state vs reconstructed projections

 Log all mismatches

 Resolve schema or semantic drift

🟠 Cutover Readiness
 Achieve 100% event parity

 Pass replay determinism tests

 Pass performance benchmarks

 Complete security review

8. Legacy Decommissioning
🔴 Finalization
 Freeze memory.db (read-only)

 Export final snapshot

 Convert snapshot → event stream

 Verify replay from snapshot produces identical state

🟠 Archival
 Archive legacy DB in cold storage

 Remove write permissions permanently

 Update documentation to mark legacy system deprecated

9. Security & Threat Modeling
🔴 Mandatory Reviews
 Memory poisoning threat model

 Event injection threat model

 Replay attack analysis

 Compromised agent scenario analysis

🟠 Hardening
 Implement anomaly detection on event streams

 Add integrity verification during replay

 Log and alert on schema violations

 Periodic key rotation plan

10. Documentation & Operations
🟠 Documentation
 Architecture diagrams (logical + physical)

 Event schema reference

 Gateway API reference

 Operator runbooks

🟢 Developer Experience
 Local dev bootstrap scripts

 Test fixtures for event replay

 Projection inspection tools

 CI checks for stateless violations

11. Post-Migration Enhancements (Deferred)
🟡 Optional Enhancements
 Multi-agent isolation via per-stream namespaces

 Cross-model shared memory via event federation

 Offline replay sandbox

 Forensic timeline visualizer

12. Exit Criteria
Migration is complete only when:

 Agent is provably stateless

 All memory is externalized and event-sourced

 Legacy storage is fully decommissioned

 Full system state can be reconstructed from events alone

 Security audit passes with no critical findings

If you want, the next logical artifacts to generate from this TODO are:

CUTOVER_CHECKLIST.md

EVENT_SCHEMAS_v1.md

MEMORY_GATEWAY_API.md

THREAT_MODEL.md

State which one to produce next.

You said:
Populate 

CUTOVER_CHECKLIST.md
EVENT_SCHEMAS_v1.md
MEMORY_GATEWAY_API.md
THREAT_MODEL.md
ChatGPT said:
Below are fully populated, production-grade versions of all four requested artifacts.
They are internally consistent, mutually referential, and aligned strictly with Option 3a: Stateless Core + Externalized, Event-Sourced Memory Services.

You can copy each section verbatim into its own file.

CUTOVER_CHECKLIST.md
Purpose:
Ensure a safe, auditable, and reversible transition from legacy stateful memory to a fully stateless, event-sourced system.

1. Pre-Cutover Preconditions (HARD GATES)
1.1 Architecture Gates
 Agent has zero direct access to databases, filesystems, or KV stores

 All agent outputs are events only

 All agent inputs are explicitly injected

 Memory Gateway is the only persistence interface

1.2 Data Gates
 All legacy memory domains mapped to canonical event types

 Event schemas finalized and versioned (v1)

 Legacy memory.db schema frozen

 Snapshot export mechanism validated

1.3 Security Gates
 Event log is append-only at the storage layer

 Hashing enabled for every event

 Write authentication enforced

 Replay integrity verification implemented

2. Shadow Mode Validation
2.1 Dual-Write Verification
 Every legacy write produces an equivalent event

 Event payloads are schema-valid

 Event timestamps are monotonic

 Event hashes are deterministic

2.2 Read Parity
 Legacy read results == projection results

 Context windows match exactly

 Knowledge retrieval parity verified

 Policy decisions identical

2.3 Replay Validation
 Full replay from genesis succeeds

 Partial replay from checkpoint succeeds

 Replay produces identical projections

 Replay time within acceptable bounds

3. Performance & Stability Gates
 Event write latency within SLA

 Projection rebuild time measured

 Gateway throughput load-tested

 Failure scenarios simulated (gateway down, projection loss)

4. Final Cutover Steps
4.1 Freeze Legacy
 Disable writes to memory.db

 Mark database read-only at filesystem level

 Export final snapshot

 Hash and archive snapshot

4.2 Activate New Path
 Disable legacy reads

 Enable projection-only reads

 Monitor gateway error rates

 Monitor projection lag

5. Post-Cutover Verification
 Agent operates without legacy DB present

 Projections rebuild successfully from events

 No state loss detected

 Security monitoring active

6. Rollback Criteria (Emergency Only)
Rollback is permitted only if:

Event corruption detected

Replay produces inconsistent state

Gateway policy failure causes data loss

Rollback steps:

Disable gateway writes

Re-enable legacy DB (read/write)

Restore snapshot

Document incident

EVENT_SCHEMAS_v1.md
Purpose:
Define the authoritative, immutable event formats used by the system.

1. Global Event Envelope (MANDATORY)
{
  "event_id": "uuid-v7",
  "event_type": "string",
  "timestamp": "ISO-8601 UTC",
  "actor": {
    "type": "agent | user | system",
    "id": "string"
  },
  "payload": {},
  "schema_version": "v1",
  "hash": "sha256(payload + metadata)"
}
No event may omit any field.

2. Event Types
2.1 ConversationEvent
{
  "event_type": "ConversationRecorded",
  "payload": {
    "conversation_id": "uuid",
    "role": "user | agent",
    "content": "string",
    "context_summary": "string | null"
  }
}
2.2 KnowledgeArtifactEvent
{
  "event_type": "KnowledgeArtifactRegistered",
  "payload": {
    "artifact_id": "uuid",
    "name": "string",
    "content_hash": "sha256",
    "tags": ["string"],
    "source": "user | system | import"
  }
}
2.3 UserPolicyEvent
{
  "event_type": "UserPolicyUpdated",
  "payload": {
    "policy_id": "uuid",
    "policy_name": "string",
    "policy_value": "json",
    "scope": "global | project | session"
  }
}
2.4 ExecutionEvent
{
  "event_type": "ToolExecuted",
  "payload": {
    "tool_name": "string",
    "command": "string",
    "exit_code": "integer",
    "duration_ms": "integer",
    "output_summary": "string"
  }
}
2.5 SystemEvent
{
  "event_type": "SystemCheckpointCreated",
  "payload": {
    "checkpoint_id": "uuid",
    "event_offset": "integer",
    "reason": "string"
  }
}
3. Versioning Rules
Schema versions are append-only

No breaking changes within a version

New fields must be optional

Deprecation requires new event type

MEMORY_GATEWAY_API.md
Purpose:
Define the only allowed interface between agents and memory.

1. Design Principles
Zero trust

Stateless

Explicit contracts

Policy-enforced

Auditable

2. API Surface
2.1 Emit Event
POST /events

{
  "event_type": "string",
  "payload": {},
  "actor": {
    "type": "agent",
    "id": "agent_id"
  }
}
Behavior:

Validates schema

Computes hash

Appends to event log

Returns event_id

2.2 Retrieve Context Snapshot
POST /context

{
  "conversation_id": "uuid",
  "window": {
    "tokens": 4000
  }
}
Returns:

{
  "context": ["string"],
  "source_projection": "conversation_context_v1"
}
2.3 Knowledge Query
POST /knowledge/search

{
  "query": "string",
  "top_k": 10
}
2.4 Policy Fetch
GET /policies?scope=session

3. Forbidden Actions
The gateway must reject:

Raw SQL

Arbitrary file access

Direct vector DB access

Stateful session writes

4. Observability
Every request logged

Every rejection logged

Correlation IDs mandatory

Metrics exposed (latency, volume, errors)

THREAT_MODEL.md
Purpose:
Identify, classify, and mitigate threats against the memory architecture.

1. Trust Boundaries
Component	Trust Level
Agent Core	Untrusted
Memory Gateway	Trusted
Event Log	Trusted
Projections	Disposable
Legacy DB	Deprecated
2. Threat Classes
2.1 Memory Poisoning
Vector: Malicious or compromised agent emits bad events
Mitigations:

Schema validation

Policy enforcement

Anomaly detection

Event signing

2.2 Replay Attacks
Vector: Re-injecting old events
Mitigations:

Event IDs + hashes

Monotonic offsets

Replay window controls

2.3 Event Log Tampering
Vector: Storage compromise
Mitigations:

Append-only storage

WORM cold archives

Hash chain verification

External audit hashes

2.4 Projection Corruption
Vector: Derived store manipulation
Mitigations:

Projections are disposable

Rebuild from events

No authority granted

2.5 Gateway Bypass
Vector: Agent attempts direct access
Mitigations:

Network isolation

Credential scoping

Static analysis of agent code

3. Incident Response Model
Freeze event ingestion

Snapshot event log

Replay to clean environment

Compare projections

Resume with verified state

4. Residual Risk
Risk	Accepted?
Gateway compromise	No
Agent misbehavior	Yes (contained)
Projection loss	Yes
Legacy DB loss	Yes
5. Security Posture Summary
This architecture:

Assumes agent compromise

Limits blast radius

Preserves forensic history

Enables deterministic recovery

Below are the **remaining populated artifacts**, completing the documentation set so that **all core and supporting artifacts** for Option 3a are now fully specified.

This response delivers **production-ready, internally consistent documents** that can be committed directly.

---

# PROJECTION_DESIGN.md

**Purpose:**
Define how immutable events are transformed into **query-optimized, disposable read models**.

---

## 1. Projection Principles

* Projections are **derived state**
* Projections have **no authority**
* Projections can be **destroyed and rebuilt**
* Events are the **single source of truth**

---

## 2. Projection Lifecycle

```
Event Log → Projection Builder → Derived Store
                      ↑
                 Replay Engine
```

Each projection:

* Subscribes to a subset of event types
* Maintains its own offset/checkpoint
* Can be rebuilt from genesis or checkpoint

---

## 3. Projection Types

### 3.1 Conversation Context Projection

**Purpose:** Provide bounded conversational context to agents.

**Input Events:**

* `ConversationRecorded`

**Derived Model (KV):**

```json
{
  "conversation_id": "uuid",
  "entries": [
    { "role": "user", "content": "…" },
    { "role": "agent", "content": "…" }
  ],
  "last_event_offset": 123456
}
```

**Rules:**

* Token-bounded window
* Old entries evicted deterministically
* No summarization without explicit events

---

### 3.2 Knowledge Search Projection

**Purpose:** Semantic retrieval.

**Input Events:**

* `KnowledgeArtifactRegistered`

**Derived Model (Vector DB):**

```json
{
  "artifact_id": "uuid",
  "embedding": [float],
  "tags": ["android", "security"],
  "content_hash": "sha256"
}
```

**Rules:**

* Embeddings regenerated on rebuild
* Content retrieved by hash from cold storage
* No mutable metadata

---

### 3.3 Tool & Execution Projection

**Purpose:** Tool visibility, diagnostics, auditing.

**Input Events:**

* `ToolExecuted`

**Derived Model (SQL):**

```sql
tool_name | executions | last_exit_code | avg_duration_ms
```

---

### 3.4 Policy Cache Projection

**Purpose:** Fast policy lookup.

**Input Events:**

* `UserPolicyUpdated`

**Rules:**

* Latest-wins per `(policy_name, scope)`
* Stateless rebuild
* Memory-resident only

---

## 4. Failure & Recovery

* Projection loss = **acceptable**
* Rebuild from event log is mandatory
* Divergence triggers rebuild, not patching

---

# EVENT_REPLAY_TOOLING.md

**Purpose:**
Enable deterministic reconstruction of system state.

---

## 1. Replay Guarantees

* Deterministic
* Order-preserving
* Side-effect free
* Idempotent

---

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

---

## 3. Replay Engine Responsibilities

* Validate schema per event
* Verify hash integrity
* Enforce ordering
* Feed events to projection builders

---

## 4. Replay Failure Handling

| Failure          | Action           |
| ---------------- | ---------------- |
| Hash mismatch    | Abort + alert    |
| Schema violation | Abort            |
| Projection error | Reset projection |

---

## 5. Audit Mode

Replay engine supports:

* Dry-run mode
* Differential comparison
* Projection diff output

---

# SECURITY_AUDIT_CHECKLIST.md

**Purpose:**
Provide a **repeatable, formal security audit process**.

---

## 1. Architecture Audit

* [ ] Agent has no persistent storage access
* [ ] Gateway enforces authentication
* [ ] Event log is append-only at storage layer
* [ ] Projections have no write-back paths

---

## 2. Event Integrity

* [ ] Hash verified for all events
* [ ] Hash algorithm approved
* [ ] No mutable fields post-write
* [ ] Schema versions enforced

---

## 3. Access Control

* [ ] Gateway credentials scoped
* [ ] Agents cannot escalate privileges
* [ ] Projection backends isolated
* [ ] Legacy DB inaccessible

---

## 4. Supply Chain

* [ ] Tooling binaries verified
* [ ] Build scripts audited
* [ ] Dependency hashes pinned

---

## 5. Incident Simulation

* [ ] Malicious agent simulation
* [ ] Projection corruption simulation
* [ ] Gateway outage simulation
* [ ] Replay-based recovery tested

---

## 6. Audit Outcome

Audit passes only if:

* No critical findings
* All high-severity findings remediated
* Replay verified end-to-end

---

# OPERATOR_RUNBOOK.md

**Purpose:**
Guide operators during **normal operation, incidents, and recovery**.

---

## 1. Normal Operations

### 1.1 Daily Checks

* Event ingestion rate
* Projection lag
* Gateway error rate

### 1.2 Weekly Checks

* Projection rebuild test
* Event log integrity scan
* Cold archive verification

---

## 2. Incident Response

### 2.1 Suspected Memory Corruption

1. Freeze event ingestion
2. Snapshot event log
3. Replay into clean environment
4. Compare projections
5. Resume or rollback

---

### 2.2 Gateway Compromise

1. Rotate credentials
2. Disable writes
3. Audit recent events
4. Rebuild projections
5. Resume with clean state

---

## 3. Disaster Recovery

* Event log is primary asset
* Projections rebuilt from scratch
* No reliance on backups beyond events

---

## 4. Operator Prohibitions

Operators **must not**:

* Modify events
* Patch projections manually
* Restore legacy DB writes
* Bypass gateway policies

---

# FINAL STATUS SUMMARY

At this point, the system has **all required artifacts populated**:

✔ `TODO.md`
✔ `CUTOVER_CHECKLIST.md`
✔ `EVENT_SCHEMAS_v1.md`
✔ `MEMORY_GATEWAY_API.md`
✔ `THREAT_MODEL.md`
✔ `PROJECTION_DESIGN.md`
✔ `EVENT_REPLAY_TOOLING.md`
✔ `SECURITY_AUDIT_CHECKLIST.md`
✔ `OPERATOR_RUNBOOK.md`

---

## Next (Optional but Strategic)

If you want to go further, the only remaining *non-code* gaps are:

* `REFERENCE_ARCHITECTURE_DIAGRAM.md`
* `COMPLIANCE_MAPPING.md` (SOC-style controls)
* `FORMAL_INVARIANTS.md` (mathematical guarantees)

If you want **code next**, the logical step is:

* Memory Gateway reference implementation
* Event replay engine
* Projection builders

State direction and language preference.
