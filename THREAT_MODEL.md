# Threat Model

Purpose: Identify, classify, and mitigate threats against the memory architecture.

## 1. Trust Boundaries

| Component      | Trust Level |
| -------------- | ----------- |
| Agent Core     | Untrusted   |
| Memory Gateway | Trusted     |
| Event Log      | Trusted     |
| Projections    | Disposable  |
| Legacy DB      | Deprecated  |

## 2. Threat Classes

### 2.1 Memory Poisoning

Vector: Malicious or compromised agent emits bad events.

Mitigations:
- Schema validation
- Policy enforcement
- Anomaly detection
- Event signing

### 2.2 Replay Attacks

Vector: Re-injecting old events.

Mitigations:
- Event IDs and hashes
- Monotonic offsets
- Replay window controls

### 2.3 Event Log Tampering

Vector: Storage compromise.

Mitigations:
- Append-only storage
- WORM cold archives
- Hash chain verification
- External audit hashes

### 2.4 Projection Corruption

Vector: Derived store manipulation.

Mitigations:
- Projections are disposable
- Rebuild from events
- No authority granted

### 2.5 Gateway Bypass

Vector: Agent attempts direct access.

Mitigations:
- Network isolation
- Credential scoping
- Static analysis of agent code

## 3. Incident Response Model

- Freeze event ingestion
- Snapshot event log
- Replay to clean environment
- Compare projections
- Resume with verified state

## 4. Residual Risk

| Risk              | Accepted?        |
| ----------------- | ---------------- |
| Gateway compromise| No               |
| Agent misbehavior | Yes (contained)  |
| Projection loss   | Yes              |
| Legacy DB loss    | Yes              |

## 5. Security Posture Summary

This architecture:
- Assumes agent compromise
- Limits blast radius
- Preserves forensic history
- Enables deterministic recovery
