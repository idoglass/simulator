# FR-GR-028

- Source GR ID: GR-028
- Priority: P0
- Status: Implemented

## Feature Requirement
Support runtime task loading and registration before execution.

## Acceptance Criteria
- New task definitions can be loaded, validated, and executed without restart.

## Implementation
- **TaskRegistryPort.register_from_path(path)** and **FileTaskRegistryAdapter.register_from_path**: load a .task.json from path, parse, and add to in-memory registry. **SimulationService.load_task(path)** and **RunWorkflow.load_task(path)** expose it. No restart required; new task is immediately get/list/executable.
