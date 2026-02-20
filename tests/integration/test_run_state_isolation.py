"""Integration test: run state isolation (TKT-C07-02)."""

from __future__ import annotations

from simulator.domain.services.run_state_factory import RunStateFactory


def test_sequential_runs_have_isolated_state() -> None:
    factory = RunStateFactory()
    c1 = factory.create(run_id="r1")
    c2 = factory.create(run_id="r2")
    c1.mutable_state["x"] = 1
    assert c2.mutable_state.get("x") is None
