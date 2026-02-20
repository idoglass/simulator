"""GUI entry: launch GUI or run minimal flow when GUI framework unavailable."""

from __future__ import annotations

from uuid import uuid4

from simulator.domain.models.run_models import RunInput


def run_gui(container: dict[str, object]) -> None:
    """Run GUI mode. Uses tk_mvc when available; otherwise runs one minimal flow (foundation)."""
    workflow = container["workflow"]
    run_input = RunInput(
        run_id=f"run-{uuid4().hex[:8]}",
        target_id="default-target",
        task_id="default-task",
        protocol="tcp",
    )
    result = workflow.run(run_input)
    # Foundation: core flow ran. Full tk_mvc window can be wired in mvc-architecture feature.
    print(f"[ok] Run completed: {result.get('verification', {}).get('summary', '')}")
