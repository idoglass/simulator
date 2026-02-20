# FR-GR-007

- Source GR ID: GR-007
- Priority: P0
- Status: Implemented

## Feature Requirement
Deliver a robust, generic, stateless desktop simulator foundation.

## Acceptance Criteria
- Core simulator flows run without coupling to one specific application model in desktop runtime mode.

## Implementation
- **Package:** `src/simulator/` with domain (models, ports), workflows (run_workflow), adapters (logging, events, verification, ui, transport stubs), app (bootstrap, entry point), config (resolve).
- **Run workflow:** `RunWorkflow.run(RunInput)` orchestrates one simulation run using VerificationPort, EventBusPort, LoggingPort; no mutable in-process state between runs; parameterized by target_id/task_id/protocol (generic).
- **Desktop entry:** `python -m simulator --tui` or `--gui` runs one minimal flow; GUI path defers to `adapters.ui.gui.main.run_gui` (foundation runs flow when tk_mvc unavailable).
- **Tests:** `tests/test_simulator_foundation.py` (unittest) verifies flow runs without app-model coupling and stateless multiple runs.
- **Build:** `pyproject.toml` at repo root; optional `pip install -e .` for console script `simulator`.
