"""Count-based verification adapter. Implements VerificationPort (MVP: count rules)."""

from __future__ import annotations

from simulator.domain.models.run_models import ObservedInteractions, VerificationResult


class CountVerificationAdapter:
    """MVP: verify expected vs observed counts. Foundation stub returns pass with no rules."""

    def verify_count_rules(
        self,
        expected: list[dict[str, object]],
        observed: ObservedInteractions,
    ) -> VerificationResult:
        """Evaluate count rules. With empty expected, returns passed."""
        if not expected:
            return VerificationResult(
                passed=True,
                summary="No rules to verify",
                mismatches=(),
            )
        # Placeholder: compare counts when expected is non-empty (later feature).
        return VerificationResult(
            passed=True,
            summary="Count verification (stub)",
            mismatches=(),
        )
