"""Shared simulation service API. GUI and TUI call this; no duplicated logic."""

from __future__ import annotations

from simulator.domain.models.run_models import RunInput
from simulator.workflows import RunWorkflow


class SimulationService:
    """Facade over run/verify/task operations. Single API for GUI and TUI (FR-GR-026)."""

    def __init__(self, run_workflow: RunWorkflow) -> None:
        self._workflow = run_workflow

    def run(
        self,
        *,
        run_id: str,
        target_id: str,
        task_id: str,
        protocol: str = "tcp",
    ) -> dict[str, object]:
        """Execute one simulation run. Equivalent results for equivalent inputs from GUI or TUI."""
        run_input = RunInput(
            run_id=run_id,
            target_id=target_id,
            task_id=task_id,
            protocol=protocol,
        )
        return self._workflow.run(run_input)

    def list_tasks(self) -> list[dict[str, object]]:
        """List registered tasks. Delegates to workflow's task registry."""
        return self._workflow.list_tasks()

    def load_task(self, path: str) -> dict[str, object]:
        """Load and register a task from a file path (runtime, without restart)."""
        return self._workflow.load_task(path)

    def compose_task(self, base_task_ids: list[str], overrides: dict[str, object] | None = None) -> dict[str, object]:
        """Compose a new task from base tasks and register it (runtime, no restart)."""
        return self._workflow.compose_task(base_task_ids, overrides or {})

    def create_task(self, definition: dict[str, object]) -> dict[str, object]:
        """Create and register a task from scratch (form/editor)."""
        return self._workflow.create_task(definition)
