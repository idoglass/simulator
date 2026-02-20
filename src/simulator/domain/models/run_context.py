"""Isolated per-run mutable state (TKT-C07-01)."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class RunContext:
    """Per-run context with unique run_id; no carryover between runs."""

    run_id: str
    correlation_id: str | None = None
    mutable_state: dict[str, Any] = field(default_factory=dict)
