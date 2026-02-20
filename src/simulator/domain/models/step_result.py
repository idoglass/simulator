"""Step execution result and lifecycle state (TKT-C03-01)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class StepResult:
    """Per-step result: order_index, state, verdict, evidence."""

    order_index: int
    state: str  # started | completed | failed
    verdict: str  # PASS | FAIL | SKIP
    evidence: dict[str, Any] | None = None
