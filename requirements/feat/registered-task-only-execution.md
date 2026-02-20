# FR-GR-023

- Source GR ID: GR-023
- Priority: P0
- Status: Implemented

## Feature Requirement
Execute simulation actions only through registered tasks.

## Acceptance Criteria
- Engine rejects execution requests for non-registered tasks.

## Implementation
- RunWorkflow resolves task via TaskRegistryPort.get(task_id); when None, returns RUN_FAILED with TASK_NOT_FOUND and verification passed=False. No execution path without a registered task.
