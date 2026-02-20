# Error Code Catalog (MVP)

This document standardizes error families, codes, user-facing message intent, and diagnostic metadata.

## 1) Goals

1. Ensure deterministic error semantics across subsystems.
2. Keep user-facing messages consistent across GUI/TUI.
3. Make logs and tests assert stable error codes, not fragile free text.

## 2) Error Envelope

All runtime errors should use a shared envelope:

```json
{
  "code": "CONFIG_PROTOCOL_INVALID",
  "message": "Protocol must be tcp or udp.",
  "category": "config",
  "severity": "error",
  "path": "targets[0].transport.protocol",
  "run_id": "optional",
  "task_id": "optional",
  "target_id": "optional",
  "details": {}
}
```

Required fields:

- `code`
- `message`
- `category`
- `severity`

Optional fields:

- `path`
- correlation IDs
- `details` (safe and redacted)

## 3) Severity Levels

- `error`: operation/run cannot continue
- `warn`: operation can continue with degraded behavior or fallback

## 4) Catalog by Category

## 4.1 Configuration (`config`)

| Code | Default User Message |
| --- | --- |
| `CONFIG_SCHEMA_INVALID` | Configuration format is invalid. |
| `CONFIG_UNKNOWN_KEY` | Configuration contains an unsupported key. |
| `CONFIG_TYPE_MISMATCH` | Configuration field type is invalid. |
| `CONFIG_TARGET_NOT_FOUND` | Target ID was not found in configuration. |
| `CONFIG_PROTOCOL_INVALID` | Protocol must be tcp or udp. |
| `CONFIG_PORT_INVALID` | Port must be between 1 and 65535. |
| `CONFIG_TIMEOUT_INVALID` | Timeout values must be positive integers. |
| `CONFIG_FRAMING_REQUIRED` | Framing configuration is required for this flow. |
| `CONFIG_COMPATIBILITY_UNSUPPORTED` | Current environment is not supported by compatibility matrix. |
| `CONFIG_OVERRIDE_INVALID` | Run override values are invalid. |

## 4.2 Task (`task`)

| Code | Default User Message |
| --- | --- |
| `TASK_PARSE_ERROR` | Task file could not be parsed. |
| `TASK_SCHEMA_INVALID` | Task file schema is invalid. |
| `TASK_SCHEMA_UNSUPPORTED` | Task schema version is not supported. |
| `TASK_ID_CONFLICT` | Task ID already exists and cannot be registered. |
| `TASK_STEPS_EMPTY` | Task must include at least one step. |
| `TASK_STEP_INVALID` | One or more task steps are invalid. |
| `TASK_MESSAGE_TYPE_UNKNOWN` | Task references an unknown message type. |
| `TASK_COMPOSITION_CYCLE` | Task composition contains a cycle. |
| `TASK_COMPOSITION_REFERENCE_MISSING` | Composed task references a missing base task. |

## 4.3 Contract (`contract`)

| Code | Default User Message |
| --- | --- |
| `CONTRACT_SOURCE_NOT_FOUND` | Contract source path was not found. |
| `CONTRACT_PARSE_FAILED` | Contract source could not be parsed. |
| `CONTRACT_SYMBOL_CONFLICT` | Contract symbols conflict across sources. |
| `CONTRACT_TYPE_UNSUPPORTED` | Contract contains unsupported type definitions. |
| `CONTRACT_VALIDATION_FAILED` | Contract validation failed. |
| `CONTRACT_BUNDLE_EMPTY` | No valid contract symbols were produced. |

## 4.4 Transport (`transport`)

| Code | Default User Message |
| --- | --- |
| `TRANSPORT_CONNECT_TIMEOUT` | Connection timed out. |
| `TRANSPORT_READ_TIMEOUT` | Read operation timed out. |
| `TRANSPORT_WRITE_TIMEOUT` | Write operation timed out. |
| `TRANSPORT_CONNECTION_REFUSED` | Connection was refused by endpoint. |
| `TRANSPORT_CONNECTION_RESET` | Connection was reset by peer. |
| `TRANSPORT_BIND_FAILED` | Failed to bind local endpoint. |
| `TRANSPORT_PROTOCOL_ERROR` | Transport protocol error occurred. |
| `TRANSPORT_RETRY_EXHAUSTED` | Retries were exhausted. |
| `TRANSPORT_CANCELLED` | Transport operation was cancelled. |

## 4.5 Verification (`verification`)

| Code | Default User Message |
| --- | --- |
| `VERIFICATION_RULE_INVALID` | Verification rule definition is invalid. |
| `VERIFICATION_MATCHER_ERROR` | Verification matcher evaluation failed. |
| `VERIFICATION_COUNT_MISMATCH` | Observed message count did not match expectation. |
| `VERIFICATION_ENGINE_FAILED` | Verification engine failed to complete. |

## 4.6 Capture/Replay (`capture_replay`)

| Code | Default User Message |
| --- | --- |
| `CAPTURE_WRITE_FAILED` | Failed to write capture artifact. |
| `CAPTURE_READ_FAILED` | Failed to read capture artifact. |
| `CAPTURE_FORMAT_INVALID` | Capture artifact format is invalid. |
| `REPLAY_METADATA_MISSING` | Replay metadata is missing or incomplete. |
| `REPLAY_EXECUTION_FAILED` | Replay execution failed. |

## 4.7 Event/Observability (`observability`)

| Code | Default User Message |
| --- | --- |
| `EVENT_DISPATCH_FAILED` | Event dispatch failed. |
| `LOG_SINK_INIT_FAILED` | Log output sink could not be initialized. |
| `REDACTION_POLICY_VIOLATION` | Sensitive data redaction policy was violated. |

## 5) UI Message Rules

1. GUI/TUI should display default user message plus code.
2. Raw technical details belong in expandable diagnostics, not headline message.
3. Sensitive values must be redacted before UI display.

## 6) Logging Rules

1. Logs must include `code`, `category`, `severity`, and correlation IDs when available.
2. Tests should assert `code` (and optionally `category`), not full message text.
3. Message text may be refined over time without changing code semantics.

## 7) Change Management

1. Error codes are additive by default; avoid renaming existing codes.
2. If deprecating a code, document replacement code and transition window.
3. Any new category/code should be reflected in relevant architecture specs and tests.

## 8) Requirement Mapping

- GR-059, GR-039, GR-040
