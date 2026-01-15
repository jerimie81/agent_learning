# Security Audit Checklist

Purpose: Provide a repeatable, formal security audit process.

## 1. Architecture Audit

- [ ] Agent has no persistent storage access.
- [ ] Gateway enforces authentication.
- [ ] Event log is append-only at storage layer.
- [ ] Projections have no write-back paths.

## 2. Event Integrity

- [ ] Hash verified for all events.
- [ ] Hash algorithm approved.
- [ ] No mutable fields post-write.
- [ ] Schema versions enforced.

## 3. Access Control

- [ ] Gateway credentials scoped.
- [ ] Agents cannot escalate privileges.
- [ ] Projection backends isolated.
- [ ] Legacy DB inaccessible.

## 4. Supply Chain

- [ ] Tooling binaries verified.
- [ ] Build scripts audited.
- [ ] Dependency hashes pinned.

## 5. Incident Simulation

- [ ] Malicious agent simulation.
- [ ] Projection corruption simulation.
- [ ] Gateway outage simulation.
- [ ] Replay-based recovery tested.

## 6. Audit Outcome

Audit passes only if:
- No critical findings.
- All high-severity findings remediated.
- Replay verified end-to-end.
