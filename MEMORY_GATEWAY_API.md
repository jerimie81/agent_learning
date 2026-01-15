# Memory Gateway API

Purpose: Define the only allowed interface between agents and memory.

## 1. Design Principles

- Zero trust
- Stateless
- Explicit contracts
- Policy enforced
- Auditable

## 2. API Surface

### 2.1 Emit Event

`POST /events`

```json
{
  "event_type": "string",
  "payload": {},
  "actor": {
    "type": "agent",
    "id": "agent_id"
  }
}
```

Behavior:
- Validates schema
- Computes hash
- Appends to event log
- Returns event_id

### 2.2 Retrieve Context Snapshot

`POST /context`

```json
{
  "conversation_id": "uuid",
  "window": {
    "tokens": 4000
  }
}
```

Returns:

```json
{
  "context": ["string"],
  "source_projection": "conversation_context_v1"
}
```

### 2.3 Knowledge Query

`POST /knowledge/search`

```json
{
  "query": "string",
  "top_k": 10
}
```

### 2.4 Policy Fetch

`GET /policies?scope=session`

## 3. Forbidden Actions

The gateway must reject:
- Raw SQL
- Arbitrary file access
- Direct vector DB access
- Stateful session writes

## 4. Observability

- Every request logged
- Every rejection logged
- Correlation IDs mandatory
- Metrics exposed (latency, volume, errors)
