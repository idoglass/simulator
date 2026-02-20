"""Workflow scaffolding template."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class RunInput:
    run_id: str
    target_id: str
    task_id: str
    protocol: str


class RunWorkflowTemplate:
    """Template run workflow orchestrator.

    Replace `Any` ports with concrete domain-port interfaces.
    """

    def __init__(
        self,
        *,
        contract_port: Any,
        task_registry_port: Any,
        transport_port: Any,
        verification_port: Any,
        event_bus: Any,
        logger: Any,
    ) -> None:
        self._contract_port = contract_port
        self._task_registry_port = task_registry_port
        self._transport_port = transport_port
        self._verification_port = verification_port
        self._event_bus = event_bus
        self._logger = logger

    def run(self, run_input: RunInput) -> dict[str, object]:
        self._event_bus.publish({"event_type": "RunStarted", "run_id": run_input.run_id})
        self._logger.info("RUN_STARTED", run_id=run_input.run_id, task_id=run_input.task_id)

        # TODO: resolve contracts and task, then execute transport.
        observed = {"interactions": [], "transport_errors": []}
        verification = self._verification_port.verify_count_rules(expected=[], observed=observed)

        self._event_bus.publish({"event_type": "RunCompleted", "run_id": run_input.run_id})
        self._logger.info("RUN_COMPLETED", run_id=run_input.run_id, passed=verification.get("passed"))

        return {
            "run_id": run_input.run_id,
            "observed": observed,
            "verification": verification,
        }

