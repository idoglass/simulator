# DDS Supporting 02: Validation and Error Model

## 1. Purpose

Define when validation occurs, how failures are categorized, and how concrete SRS error codes are emitted.

## 2. Validation Phases

1. **CRUD-time validation**
   - field types, ranges, enum values
   - reference existence (`*_ref`)
   - uniqueness constraints

2. **Pre-run validation**
   - resolved run bundle integrity
   - task registration checks
   - transport endpoint validity
   - periodic config validity

3. **Runtime validation**
   - transport outcome validity
   - verification rule execution
   - scheduler overlap handling

## 3. Error Envelope

All errors use normalized envelope:

```text
{
  error_code,
  category,
  message,
  entity_type,
  entity_id,
  run_id,
  step_id,
  timestamp_utc,
  recoverable
}
```

## 4. Category Routing

- `VALIDATION_ERROR` -> input/config issues
- `TASK_REGISTRATION_ERROR` -> task lookup/load failures
- `TRANSPORT_ERROR` -> send/receive/connection failures
- `VERIFICATION_ERROR` -> expectation mismatch failures
- `RUN_POLICY_ERROR` -> stop/skip/queue policy outcomes
- `INTERNAL_ERROR` -> unhandled internal failures

## 5. Code Mapping Reference

SRS section 11.1 is the source-of-truth table:

- `SRS-E-VAL-*`
- `SRS-E-TASK-*`
- `SRS-E-TRN-*`
- `SRS-E-VER-*`
- `SRS-E-RUN-*`
- `SRS-E-INT-*`

## 6. Recoverability Semantics

- recoverable errors should preserve process availability and allow corrected retry
- non-recoverable errors terminate current run context safely and emit full diagnostics

## 7. UI and Logging Behavior

- UI must show `error_code` and concise actionable message.
- Logs must include full envelope plus contextual metadata.
- Sensitive fields in payloads must be redacted before emission.
