"""Verification port contract. Adapters implement expected-vs-observed evaluation."""

from __future__ import annotations

from typing import TYPE_CHECKING, Protocol

if TYPE_CHECKING:
    from simulator.domain.models.run_models import ObservedInteractions, VerificationResult


class VerificationPort(Protocol):
    """Evaluate expected vs observed interactions (MVP: count-based rules)."""

    def verify_count_rules(
        self,
        expected: list[dict[str, object]],
        observed: "ObservedInteractions",
    ) -> "VerificationResult": ...
