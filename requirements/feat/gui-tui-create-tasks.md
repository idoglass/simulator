# GUI and TUI create tasks

- Source GR ID: GR-027, GR-028
- Priority: P0
- Status: Implemented

## Feature Requirement
Allow users to create tasks from GUI and TUI: load from file, compose from existing tasks, create from scratch.

## Acceptance Criteria
- Load task from file path in both GUI and TUI (path selection in GUI; path input or API in TUI).
- Compose a new task from one or more registered tasks in both GUI and TUI.
- Create a new task from scratch (form/editor) in both GUI and TUI.
- Created/composed tasks are registered via the shared engine and immediately listable and runnable.

## Implementation
- **Load:** `SimulationService.load_task(path)`; GUI uses file dialog; TUI shows path hint and supports path input.
- **Compose:** `SimulationService.compose_task(base_task_ids, overrides)`; `TaskRegistryPort.compose()` in FileTaskRegistryAdapter; GUI/TUI buttons call service with selected bases.
- **Create from scratch:** `SimulationService.create_task(definition)`; `TaskRegistryPort.register_definition()`; GUI form (task_id, name, steps JSON); TUI creates minimal task (tui-created-1) on Create button.
- All three flows use the same engine; validation and registration are shared.
