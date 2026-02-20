"""RunStateFactory: create isolated run context per run (TKT-C07-01)."""

from __future__ import annotations

import uuid

from simulator.domain.models.run_context import RunContext


class RunStateFactory:
    """Creates fresh mutable state per run; no shared state between runs."""

    def create(self, run_id: str | None = None, correlation_id: str | None = None) -> RunContext:
        rid = run_id or str(uuid.uuid4())
        return RunContext(run_id=rid, correlation_id=correlation_id)
