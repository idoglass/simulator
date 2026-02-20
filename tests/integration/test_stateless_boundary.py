"""Integration test: stateless boundary (TKT-S04-02)."""

from __future__ import annotations

from simulator.domain.services.run_state_factory import RunStateFactory


def test_fresh_state_per_run() -> None:
    f = RunStateFactory()
    a = f.create(run_id="a")
    b = f.create(run_id="b")
    assert a.run_id != b.run_id
