"""Unit tests for RunStateFactory (TKT-C07-01)."""

from __future__ import annotations

from simulator.domain.services.run_state_factory import RunStateFactory


def test_every_run_gets_fresh_state_with_unique_id() -> None:
    factory = RunStateFactory()
    ctx1 = factory.create(run_id="run-1")
    ctx2 = factory.create(run_id="run-2")
    assert ctx1.run_id == "run-1"
    assert ctx2.run_id == "run-2"
    assert ctx1.mutable_state is not ctx2.mutable_state


def test_create_without_run_id_generates_unique() -> None:
    factory = RunStateFactory()
    ctx = factory.create()
    assert ctx.run_id and len(ctx.run_id) > 0
