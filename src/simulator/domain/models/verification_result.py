"""Verification result with evidence payload and error mapping (TKT-C06-02)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class VerificationEvidence:
    """Structured evidence; failed verification includes summary and code mapping."""

    passed: bool
    summary: str
    code: str | None = None  # SRS-E-VER-001 etc.
    details: dict[str, Any] | None = None
