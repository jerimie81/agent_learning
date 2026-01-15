# Projection Design

Purpose: Define how immutable events are transformed into query-optimized, disposable read models.

## 1. Projection Principles

- Projections are derived state.
- Projections have no authority.
- Projections can be destroyed and rebuilt.
- Events are the single source of truth.

## 2. Projection Lifecycle

```
Event Log -> Projection Builder -> Derived Store
                     ^
                Replay Engine
```

Each projection:
- Subscribes to a subset of event types.
- Maintains its own offset or checkpoint.
- Can be rebuilt from genesis or checkpoint.

## 3. Projection Types

### 3.1 Conversation Context Projection

Purpose: Provide bounded conversational context to agents.

Input events:
- ConversationRecorded

Derived model (KV):

```json
{
  "conversation_id": "uuid",
  "entries": [
    { "role": "user", "content": "..." },
    { "role": "agent", "content": "..." }
  ],
  "last_event_offset": 123456
}
```

Rules:
- Token-bounded window.
- Old entries evicted deterministically.
- No summarization without explicit events.

### 3.2 Knowledge Search Projection

Purpose: Semantic retrieval.

Input events:
- KnowledgeArtifactRegistered

Derived model (vector DB):

```json
{
  "artifact_id": "uuid",
  "embedding": [0.01, 0.02, 0.03],
  "tags": ["android", "security"],
  "content_hash": "sha256"
}
```

Rules:
- Embeddings regenerated on rebuild.
- Content retrieved by hash from cold storage.
- No mutable metadata.

### 3.3 Tool and Execution Projection

Purpose: Tool visibility, diagnostics, auditing.

Input events:
- ToolExecuted

Derived model (SQL):

```sql
tool_name | executions | last_exit_code | avg_duration_ms
```

### 3.4 Policy Cache Projection

Purpose: Fast policy lookup.

Input events:
- UserPolicyUpdated

Rules:
- Latest-wins per (policy_name, scope).
- Stateless rebuild.
- Memory-resident only.

## 4. Failure and Recovery

- Projection loss is acceptable.
- Rebuild from event log is mandatory.
- Divergence triggers rebuild, not patching.
