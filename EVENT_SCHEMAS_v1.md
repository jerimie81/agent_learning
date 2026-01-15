# Event Schemas v1

Purpose: Define the authoritative, immutable event formats used by the system.

## 1. Global Event Envelope (Mandatory)

```json
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
```

No event may omit any field.

## 2. Event Types

### 2.1 ConversationEvent

```json
{
  "event_type": "ConversationRecorded",
  "payload": {
    "conversation_id": "uuid",
    "role": "user | agent",
    "content": "string",
    "context_summary": "string | null"
  }
}
```

### 2.2 KnowledgeArtifactEvent

```json
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
```

### 2.3 UserPolicyEvent

```json
{
  "event_type": "UserPolicyUpdated",
  "payload": {
    "policy_id": "uuid",
    "policy_name": "string",
    "policy_value": "json",
    "scope": "global | project | session"
  }
}
```

### 2.4 ExecutionEvent

```json
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
```

### 2.5 SystemEvent

```json
{
  "event_type": "SystemCheckpointCreated",
  "payload": {
    "checkpoint_id": "uuid",
    "event_offset": "integer",
    "reason": "string"
  }
}
```

## 3. Versioning Rules

- Schema versions are append-only.
- No breaking changes within a version.
- New fields must be optional.
- Deprecation requires a new event type.
