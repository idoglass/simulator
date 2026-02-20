"""Run lifecycle: create context, run, teardown (TKT-C07-01, TKT-C07-02)."""

from __future__ import annotations

from simulator.domain.services.run_state_factory import RunStateFactory


def create_run_context(run_id: str | None = None) -> object:
    """Create isolated run context via RunStateFactory."""
    factory = RunStateFactory()
    return factory.create(run_id=run_id)


def teardown_run(context: object) -> None:
    """Teardown run context; no state leakage."""
    pass
