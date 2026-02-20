# FR-GR-059

- Source GR ID: GR-059
- Priority: P0
- Status: Implemented

## Feature Requirement
Emit verbose lifecycle logs with configurable levels and sensitive-data redaction.

## Acceptance Criteria
- Required events are logged, log levels are configurable at runtime, and sensitive values are redacted.

## Implementation
- **ConsoleLoggingAdapter** logs RUN_STARTED, RUN_COMPLETED (and RUN_FAILED from workflow). **_redact** redacts sensitive keys (password, secret, token, api_key, etc.) to [REDACTED]; correlation fields (run_id, task_id, target_id) preserved. Log level follows Python logging (configurable via logging.getLogger).
