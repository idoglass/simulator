"""Run-related domain models. Generic (no coupling to one application model)."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class RunInput:
    """Input for one simulation run. Parameterized by target/task/protocol."""

    run_id: str
    target_id: str
    task_id: str
    protocol: str


@dataclass(frozen=True)
class ObservedInteractions:
    """Ordered observations from transport execution (generic)."""

    interactions: tuple[dict[str, object], ...]
    transport_errors: tuple[str, ...]


@dataclass(frozen=True)
class VerificationResult:
    """Result of expected-vs-observed evaluation (generic)."""

    passed: bool
    summary: str
    mismatches: tuple[dict[str, object], ...]
