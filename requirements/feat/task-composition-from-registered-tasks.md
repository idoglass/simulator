# FR-GR-027

- Source GR ID: GR-027
- Priority: P0
- Status: Implemented

## Feature Requirement
Support creation of user-defined tasks from existing registered tasks.

## Acceptance Criteria
- Task composition creates valid reusable tasks with unique task IDs.

## Implementation
- TaskRegistryPort.compose(base_task_ids, overrides); FileTaskRegistryAdapter merges steps/payloads/defaults; SimulationService.compose_task(); GUI and TUI expose Compose. Rejects duplicate ID and missing base.
