"""Count-based verification adapter. Implements VerificationPort (MVP: count rules)."""

from __future__ import annotations

from simulator.domain.models.run_models import ObservedInteractions, VerificationResult


def _count_by_type(interactions: tuple[dict[str, object], ...], message_type: str, direction: str) -> int:
    """Count interactions matching direction; if message_type given, filter by it when present."""
    n = 0
    for i in interactions:
        if i.get("direction") != direction:
            continue
        if message_type and i.get("message_type") != message_type:
            continue
        n += 1
    return n


class CountVerificationAdapter:
    """MVP: verify expected vs observed counts (count-based rules)."""

    def verify_count_rules(
        self,
        expected: list[dict[str, object]],
        observed: ObservedInteractions,
    ) -> VerificationResult:
        """Evaluate count rules. Each expected has message_type, direction, expected_count, comparison."""
        if not expected:
            return VerificationResult(
                passed=True,
                summary="No rules to verify",
                mismatches=(),
            )
        mismatches: list[dict[str, object]] = []
        for rule in expected:
            msg_type = str(rule.get("message_type", ""))
            direction = str(rule.get("direction", "receive"))
            want = int(rule.get("expected_count", 0))
            comparison = str(rule.get("comparison", "eq"))
            actual = _count_by_type(observed.interactions, msg_type, direction)
            passed_rule = (comparison == "eq" and actual == want) or (
                comparison == "ge" and actual >= want
            )
            if not passed_rule:
                mismatches.append({
                    "message_type": msg_type,
                    "direction": direction,
                    "expected_count": want,
                    "actual_count": actual,
                    "comparison": comparison,
                })
        return VerificationResult(
            passed=len(mismatches) == 0,
            summary=f"{len(expected)} rule(s), {len(mismatches)} mismatch(es)" if mismatches else "All count rules passed",
            mismatches=tuple(mismatches),
        )
