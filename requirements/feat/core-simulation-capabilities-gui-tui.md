# FR-GR-025

- Source GR ID: GR-025
- Priority: P0
- Status: Implemented

## Feature Requirement
Expose core simulation capabilities in both GUI and TUI.

## Acceptance Criteria
- Equivalent core operations are accessible from both interfaces.

## Implementation
- Run and list tasks available in both: GUI (run_gui) and TUI (SimulatorTuiApp run/list actions) call **SimulationService.run** and **SimulationService.list_tasks**. Load task (runtime) via **SimulationService.load_task(path)**. Same API for both interfaces.
