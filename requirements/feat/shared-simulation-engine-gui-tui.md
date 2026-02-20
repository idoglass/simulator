# FR-GR-026

- Source GR ID: GR-026
- Priority: P0
- Status: Implemented

## Feature Requirement
Use one shared simulation engine for GUI and TUI paths.

## Acceptance Criteria
- GUI and TUI call shared engine APIs and produce equivalent results for equivalent inputs.

## Implementation Plan (MVP)

1. Define a shared simulation service API for run/verify/task operations.
2. Implement GUI adapters (Tkinter via `tk-mvc`) and TUI adapters (Textual) against the same API.
3. Add parity tests for equivalent GUI and TUI inputs.
4. Block direct business logic in UI layers.

## Implementation
- **SimulationService** (`domain/services/simulation_service.py`) exposes `run(run_id, target_id, task_id, protocol)` and `list_tasks()`; GUI and TUI call it via `container["simulation_service"]`. Same API, equivalent results for equivalent inputs.
