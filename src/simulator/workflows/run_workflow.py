"""Run workflow: orchestrate one simulation run. Generic, stateless, no app-model coupling."""

from __future__ import annotations

from simulator.domain.models.run_models import (
    ObservedInteractions,
    RunInput,
    VerificationResult,
)
from simulator.domain.ports import EventBusPort, LoggingPort, VerificationPort


class RunWorkflow:
    """Orchestrates a single simulation run using ports. Stateless; no mutable in-process state between runs."""

    def __init__(
        self,
        *,
        verification_port: VerificationPort,
        event_bus: EventBusPort,
        logger: LoggingPort,
    ) -> None:
        self._verification = verification_port
        self._event_bus = event_bus
        self._logger = logger

    def run(self, run_input: RunInput) -> dict[str, object]:
        """Execute one run. Parameterized by run_input only; no coupling to one application model."""
        self._event_bus.publish(
            {"event_type": "RunStarted", "run_id": run_input.run_id}
        )
        self._logger.info(
            "RUN_STARTED",
            run_id=run_input.run_id,
            target_id=run_input.target_id,
            task_id=run_input.task_id,
        )

        # Generic flow: observe (stub returns empty until transport adapter is wired), then verify.
        observed = ObservedInteractions(
            interactions=(),
            transport_errors=(),
        )
        verification: VerificationResult = self._verification.verify_count_rules(
            expected=[],
            observed=observed,
        )

        self._event_bus.publish(
            {"event_type": "RunCompleted", "run_id": run_input.run_id}
        )
        self._logger.info(
            "RUN_COMPLETED",
            run_id=run_input.run_id,
            passed=verification.passed,
        )

        return {
            "run_id": run_input.run_id,
            "observed": {
                "interactions": list(observed.interactions),
                "transport_errors": list(observed.transport_errors),
            },
            "verification": {
                "passed": verification.passed,
                "summary": verification.summary,
                "mismatches": list(verification.mismatches),
            },
        }
