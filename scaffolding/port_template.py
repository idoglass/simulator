"""Port scaffolding template."""

from __future__ import annotations

from typing import Protocol


class ExampleResult(Protocol):
    """Template result protocol shape."""

    code: str
    ok: bool


class ExamplePort(Protocol):
    """Template port contract.

    Replace this with a concrete domain port in `src/simulator/domain/ports`.
    """

    def execute(self, *, run_id: str, payload: dict[str, object]) -> dict[str, object]:
        """Execute a boundary operation and return deterministic result envelope."""

