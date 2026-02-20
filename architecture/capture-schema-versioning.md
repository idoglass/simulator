# Capture Artifact Schema and Versioning (MVP)

This document defines the file schema, compatibility rules, validation behavior, and migration policy for capture artifacts.

## 1) Scope

- Applies to capture files produced by run/capture workflow.
- Applies to replay input loading and validation.
- Ensures long-term replay compatibility as schema evolves.

## 2) Artifact Format

- Format: JSON
- Encoding: UTF-8
- File extension: `.capture.json`

## 3) Canonical Capture Shape (v1)

```json
{
  "capture_schema_version": "1.0.0",
  "capture_id": "cap-20260219-0001",
  "created_at": "2026-02-19T12:00:00Z",
  "producer": {
    "app_name": "simulator",
    "app_version": "0.1.0"
  },
  "context": {
    "run_id": "run-123",
    "target_id": "target-a",
    "task_id": "task-1",
    "task_version": "1.0.0",
    "protocol": "tcp",
    "mode": "client"
  },
  "verification_context": {
    "rules_source": "capture_metadata",
    "rule_ids": ["rule-1", "rule-2"]
  },
  "interactions": [
    {
      "index": 0,
      "timestamp": "2026-02-19T12:00:01Z",
      "direction": "send",
      "message_type": "PingRequest",
      "headers": {},
      "payload": {}
    }
  ],
  "transport_errors": [],
  "redaction": {
    "policy_version": "1",
    "redacted_fields": []
  }
}
```

## 4) Required Fields (v1)

Top-level required fields:

- `capture_schema_version`
- `capture_id`
- `created_at`
- `context`
- `interactions`

Required `context` fields:

- `run_id`
- `target_id`
- `task_id`
- `protocol`
- `mode`

Required interaction fields:

- `index` (monotonic integer starting at 0)
- `timestamp`
- `direction`
- `message_type`

## 5) Versioning Policy

Schema version uses semantic versioning: `MAJOR.MINOR.PATCH`.

Compatibility rules:

1. MVP loader supports `1.x.x`.
2. Minor/patch updates in same major must be backward compatible.
3. Unknown major versions fail validation (`CAPTURE_SCHEMA_UNSUPPORTED`).
4. Replay code must validate schema version before processing interactions.

## 6) Determinism Rules for Replay

1. Replay order follows `interactions` list order exactly.
2. Interaction `index` must be monotonic and gap-free.
3. Replay-critical metadata (`protocol`, `target_id`, `task_id`) must be present.
4. Missing required metadata causes replay validation failure before transport execution.

## 7) Validation and Error Semantics

Capture load validation categories:

- parse/format errors
- schema/version compatibility errors
- required-field presence/type errors
- interaction ordering errors

Expected error codes:

- `CAPTURE_READ_FAILED`
- `CAPTURE_FORMAT_INVALID`
- `CAPTURE_SCHEMA_UNSUPPORTED`
- `REPLAY_METADATA_MISSING`
- `REPLAY_EXECUTION_FAILED`

## 8) Migration Policy

When schema major version changes:

1. Provide explicit migration utility from prior supported major versions when feasible.
2. Migration must preserve interaction order and replay-critical context fields.
3. Migration report should include:
   - source version
   - target version
   - transformed fields
   - dropped/unsupported fields
4. Failed migration must not produce partial output artifacts.

## 9) Storage and Retention Notes

1. Capture files should be written atomically (temp file + rename).
2. Large capture files should support chunked/streaming processing in implementation.
3. Retention policy (count/size/age) should be configurable by runtime settings.

## 10) Requirement Mapping

- GR-029, GR-030, GR-031, GR-059
