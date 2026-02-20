"""Execution orchestrator: builds run plan and coordinates step execution.

SRS-FR-005, SRS-FR-020. Delegates to RunWorkflow for sequence execution.
"""

from __future__ import annotations

from simulator.domain.models.run_models import RunInput
from simulator.workflows.run_workflow import RunWorkflow


class ExecutionOrchestrator:
    """Coordinates run execution; services are composed via container."""

    def __init__(self, workflow: RunWorkflow) -> None:
        self._workflow = workflow

    def start(self, run_id: str, target_id: str, task_id: str, protocol: str = "tcp") -> dict[str, object]:
        """Start a run (sequence of one task for MVP); returns run result."""
        run_input = RunInput(run_id=run_id, target_id=target_id, task_id=task_id, protocol=protocol)
        return self._workflow.run(run_input)
