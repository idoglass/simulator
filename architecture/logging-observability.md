# Logging, Observability, and Redaction Specification (MVP)

This document defines required logs, correlation fields, event taxonomy, and sensitive-data redaction policy.

## 1) Scope

- Applies to GUI and TUI runs, capture/replay flows, runtime task loading, contract loading, verification, and transport execution.
- Covers application logs (structured) and user-visible diagnostic summaries.
- MVP focuses on local process observability.

## 2) Logging Goals

1. High signal for debugging and support.
2. Deterministic, machine-readable structure.
3. End-to-end traceability with correlation IDs.
4. Mandatory redaction of sensitive data.

## 3) Required Log Structure

All structured log records must include:

- `timestamp` (ISO-8601 UTC)
- `level` (`DEBUG`, `INFO`, `WARN`, `ERROR`)
- `event_name`
- `message`
- `run_id` (when applicable)
- `task_id` (when applicable)
- `target_id` (when applicable)
- `protocol` (when applicable)
- `component` (for example `workflow.run`, `adapter.transport.tcp`)
- `event_id` (stable ID for dedupe and trace joins)

Optional:

- `error_code`
- `duration_ms`
- `attempt`
- `metadata` (already redacted)

## 4) Event Taxonomy (Minimum Required)

### 4.1 Run Lifecycle

- `RUN_STARTED`
- `RUN_COMPLETED`
- `RUN_FAILED`
- `RUN_CANCELLED`

### 4.2 Task Lifecycle

- `TASK_LOAD_REQUESTED`
- `TASK_LOAD_SUCCEEDED`
- `TASK_LOAD_FAILED`
- `TASK_REGISTERED`
- `TASK_COMPOSED`

### 4.3 Contract Lifecycle

- `CONTRACT_LOAD_REQUESTED`
- `CONTRACT_LOAD_SUCCEEDED`
- `CONTRACT_VALIDATION_FAILED`

### 4.4 Transport Lifecycle

- `TRANSPORT_CONNECT_STARTED`
- `TRANSPORT_CONNECT_FAILED`
- `TRANSPORT_MESSAGE_SENT`
- `TRANSPORT_MESSAGE_RECEIVED`
- `TRANSPORT_TIMEOUT`
- `TRANSPORT_RETRY`

### 4.5 Verification Lifecycle

- `VERIFICATION_STARTED`
- `VERIFICATION_PASSED`
- `VERIFICATION_FAILED`

### 4.6 Capture/Replay Lifecycle

- `CAPTURE_WRITE_STARTED`
- `CAPTURE_WRITE_COMPLETED`
- `REPLAY_STARTED`
- `REPLAY_COMPLETED`
- `REPLAY_FAILED`

### 4.7 Configuration/Environment

- `CONFIG_RESOLVED`
- `CONFIG_VALIDATION_FAILED`
- `ENV_COMPATIBILITY_FAILED`

## 5) Log Levels and Emission Rules

1. `DEBUG`: detailed diagnostic flow, internal decisions, and bounded payload metadata.
2. `INFO`: major lifecycle events and successful checkpoints.
3. `WARN`: recoverable issues, retries, degraded behavior.
4. `ERROR`: failures causing run or operation failure.

Rules:

- Default runtime level is `INFO`.
- Runtime level override is allowed per run.
- Required lifecycle events must still emit at configured levels.

## 6) Redaction Policy

Sensitive data must not be emitted in plaintext logs.

### 6.1 Sensitive Data Classes

- credentials (tokens, passwords, API keys)
- personal data fields (where present in payloads)
- secret headers/metadata
- file paths containing user-private identifiers (when avoidable)

### 6.2 Redaction Rules

1. Redaction occurs before serialization to logs.
2. Known secret field names are masked fully.
3. Potentially sensitive free-text fields are truncated and flagged.
4. Large payload fields are summarized with size/hash, not full content, at non-debug levels.
5. Debug mode does not bypass redaction requirements.

### 6.3 Redaction Markers

- Use consistent marker format: `"[REDACTED]"`.
- Include optional metadata: `redacted_fields=["password","token"]`.

## 7) UI Exposure Rules

1. GUI/TUI must display high-level run/verification outcomes and key error codes.
2. GUI/TUI help/man documentation should explain log levels and redaction behavior.
3. Raw verbose logs may be exported to file for diagnostics.
4. User-facing summaries must avoid exposing sensitive payload contents.

## 8) Correlation and Traceability

1. `run_id`, `task_id`, and `target_id` must appear consistently across run logs.
2. Retries and transport attempts should include stable correlation context.
3. Verification mismatch entries should reference originating run and rule IDs.

## 9) Storage and Rotation (MVP)

1. Support console output and local file sink.
2. File sink should use bounded rotation policy by size.
3. Rotation configuration belongs to runtime config model.
4. Failure to initialize file sink must not block startup if console sink is available (emit warning).

## 10) Architecture-Level Test Expectations

Minimum tests:

1. required fields are present in lifecycle logs
2. correlation IDs propagate from run start to verification completion
3. sensitive field redaction is enforced across levels
4. transport timeout/retry emits expected event names and error codes
5. GUI/TUI summary output excludes sensitive raw payload values

## 11) Requirement Mapping

- GR-057, GR-059, GR-026, GR-039
