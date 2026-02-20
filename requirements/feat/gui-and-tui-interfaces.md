# FR-GR-012

- Source GR ID: GR-012
- Priority: P0
- Status: Implemented

## Feature Requirement
Provide both GUI and TUI interfaces for simulator usage using designated frameworks.

## Acceptance Criteria
- Feature behavior is available through GUI (`py-gui`/`tk-mvc`) and TUI (Textual) entry points.

## Implementation
- **Entry points:** `python -m simulator --gui` and `python -m simulator --tui`. GUI uses `adapters/ui/gui/main` (run via shared service); TUI uses `adapters/ui/tui/main` (Textual app with Run/List tasks, optional dep `textual`). Both call **SimulationService** only; no duplicated core logic. Fallback: if Textual not installed, --tui runs one CLI flow.
