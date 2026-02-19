# Task Format Decision and Versioning (MVP)

This document defines the task file format, schema versioning, compatibility policy, and runtime validation behavior.

## 1) Decision Summary

- **Chosen format:** JSON
- **Rationale:** deterministic parsing, strong tooling support in Python, easy schema validation, and portable behavior across Windows/Linux.
- **File extension:** `.task.json`
- **Encoding:** UTF-8

## 2) Scope

This spec applies to:

1. built-in tasks represented in file form
2. user-provided runtime task files
3. composed tasks generated from existing tasks

## 3) Canonical Task Document Shape (v1)

```json
{
  "task_schema_version": "1.0.0",
  "task_id": "ping-smoke",
  "name": "Ping Smoke",
  "description": "Simple transport smoke flow",
  "base_task_ids": [],
  "metadata": {
    "author": "team",
    "tags": ["smoke", "tcp"],
    "created_at": "2026-02-19T00:00:00Z"
  },
  "preconditions": [],
  "steps": [
    {
      "step_id": "s1",
      "action": "send",
      "message_type": "PingRequest",
      "payload_ref": "payloads.req1",
      "expect": {
        "matcher": {
          "direction": "receive",
          "message_type": "PingResponse"
        },
        "expected_count": 1,
        "comparison": "eq"
      },
      "timeout_ms": 1000
    }
  ],
  "payloads": {
    "req1": {
      "id": 1,
      "body": "hello"
    }
  },
  "defaults": {
    "protocol": "tcp",
    "mode": "client",
    "capture_enabled": false
  }
}
```

## 4) Required Fields (v1)

Required top-level fields:

- `task_schema_version`
- `task_id`
- `name`
- `steps`

Required step fields:

- `step_id`
- `action` (MVP baseline: `send`, `receive_expectation`)
- `message_type`

## 5) Composition and Extension Rules

1. `base_task_ids` is optional and may reference one or more existing registered tasks.
2. Composition resolves in deterministic order by listed `base_task_ids`.
3. Field overrides are allowed only in explicit override blocks produced by composition tooling.
4. Cyclic base references are rejected.
5. Composition output is materialized as a normalized task definition before registration.

## 6) Versioning Policy

Versioning uses semantic versioning for the schema field:

- `MAJOR.MINOR.PATCH`

Compatibility rules:

1. Loader MUST support `1.x.x` for MVP.
2. Patch and minor updates in the same major version must be backward compatible.
3. Major version changes are not auto-loaded unless explicit support is added.
4. Unknown major version -> validation failure (`TASK_SCHEMA_UNSUPPORTED`).

## 7) Validation Rules

Task file validation occurs before registration:

1. JSON must parse successfully.
2. Required top-level fields must exist with correct types.
3. `task_id` must be unique in registry scope unless explicit replacement policy is requested.
4. `steps` must be non-empty.
5. Step IDs must be unique within a task.
6. `message_type` references must resolve against loaded contract bundle.
7. `expect` blocks must follow verification spec (`architecture/verification-spec.md`).
8. Composition references must resolve and be acyclic.
9. Validation failures prevent registration (no partial registration state).

## 8) Deterministic Error Codes

- `TASK_PARSE_ERROR`
- `TASK_SCHEMA_INVALID`
- `TASK_SCHEMA_UNSUPPORTED`
- `TASK_ID_CONFLICT`
- `TASK_STEPS_EMPTY`
- `TASK_STEP_INVALID`
- `TASK_MESSAGE_TYPE_UNKNOWN`
- `TASK_COMPOSITION_CYCLE`
- `TASK_COMPOSITION_REFERENCE_MISSING`

Each error should include:

- `code`
- `message`
- `task_id` (when available)
- `path` (JSON path)

## 9) Runtime Loading and Atomic Registration

1. Load file content.
2. Parse and validate against schema/version rules.
3. Normalize composed/extended structure.
4. Validate contract references.
5. Register atomically in task registry.

If any step fails, registry remains unchanged.

## 10) Migration Guidance

For schema upgrades:

1. Provide a migration utility from prior major versions where practical.
2. Preserve task semantics and IDs unless an explicit breaking change is declared.
3. Emit migration report (`changed_fields`, `warnings`, `manual_actions`).

## 11) Requirement Mapping

- GR-027, GR-028, GR-023, GR-030
