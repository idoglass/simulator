"""Standardized error envelope (TKT-S02-02)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class ErrorEnvelope:
    """All emitted errors conform to required envelope fields and codes."""

    code: str
    category: str
    message: str
    run_id: str | None = None
    context: dict[str, Any] | None = None
