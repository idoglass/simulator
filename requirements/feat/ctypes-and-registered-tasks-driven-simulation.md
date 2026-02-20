# FR-GR-009

- Source GR ID: GR-009
- Priority: P0
- Status: Implemented

## Feature Requirement
Drive simulation only from `.h`/`ctypes` definitions and registered tasks.

## Acceptance Criteria
- Runs fail validation when message or task definitions are outside allowed sources.

## Implementation
- Execution driven by registered tasks only (TaskRegistryPort); workflow rejects run when task not found. Contract validation (`.h`/ctypes) is not yet enforced; message shapes from task payloads (MVP).
