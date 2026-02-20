"""Run workflow: orchestrate one simulation run. Generic, stateless, no app-model coupling."""

from __future__ import annotations

from typing import Callable

from simulator.domain.models.run_models import (
    ObservedInteractions,
    RunInput,
    VerificationResult,
)
from simulator.domain.models.target_and_task import (
    MessageEnvelope,
    TargetRef,
    TaskDefinition,
)
from simulator.domain.ports import (
    CaptureReplayPort,
    EventBusPort,
    LoggingPort,
    TaskRegistryPort,
    TransportPort,
    VerificationPort,
)


def _task_to_messages(task: TaskDefinition) -> list[MessageEnvelope]:
    """Build ordered message list from task steps (send steps only for outbound)."""
    messages: list[MessageEnvelope] = []
    for step in task.steps:
        if step.action == "send":
            payload = task.payloads.get(step.payload_ref or "") or {}
            messages.append(
                MessageEnvelope(
                    message_type=step.message_type,
                    direction="send",
                    payload=payload,
                )
            )
        elif step.action == "receive_expectation" and step.expect:
            messages.append(
                MessageEnvelope(
                    message_type=step.expect.message_type,
                    direction="receive",
                    payload={},
                )
            )
    return messages


def _task_to_expected_rules(task: TaskDefinition) -> list[dict[str, object]]:
    """Build expected count rules from task steps (expect blocks)."""
    rules: list[dict[str, object]] = []
    for step in task.steps:
        if step.expect:
            rules.append({
                "message_type": step.expect.message_type,
                "direction": step.expect.direction,
                "expected_count": step.expect.expected_count,
                "comparison": step.expect.comparison,
            })
    return rules


class RunWorkflow:
    """Orchestrates a single simulation run using ports. Stateless; no mutable in-process state between runs."""

    def __init__(
        self,
        *,
        verification_port: VerificationPort,
        event_bus: EventBusPort,
        logger: LoggingPort,
        transport_port: TransportPort | None = None,
        task_registry_port: TaskRegistryPort | None = None,
        target_resolver: Callable[[str], TargetRef | None] | None = None,
        capture_replay_port: CaptureReplayPort | None = None,
    ) -> None:
        self._verification = verification_port
        self._event_bus = event_bus
        self._logger = logger
        self._transport = transport_port
        self._task_registry = task_registry_port
        self._target_resolver = target_resolver
        self._capture_replay = capture_replay_port

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

        # Resolve target (target-based execution)
        target: TargetRef | None = None
        if self._target_resolver:
            target = self._target_resolver(run_input.target_id)
        if not target:
            self._logger.error("RUN_FAILED", run_id=run_input.run_id, error="TARGET_NOT_FOUND")
            return {
                "run_id": run_input.run_id,
                "observed": {"interactions": [], "transport_errors": ["TARGET_NOT_FOUND"]},
                "verification": {"passed": False, "summary": "Target not found", "mismatches": []},
            }

        # Resolve task (registered-task-only execution)
        task: TaskDefinition | None = None
        if self._task_registry:
            task = self._task_registry.get(run_input.task_id)
        if not task:
            self._logger.error("RUN_FAILED", run_id=run_input.run_id, error="TASK_NOT_FOUND")
            return {
                "run_id": run_input.run_id,
                "observed": {"interactions": [], "transport_errors": ["TASK_NOT_FOUND"]},
                "verification": {"passed": False, "summary": "Task not found", "mismatches": []},
            }

        protocol = run_input.protocol or str(task.defaults.get("protocol") or "tcp")
        timeout_ms = max((s.timeout_ms for s in task.steps), default=5000)

        # Transport execution (UDP/TCP)
        if self._transport:
            messages = _task_to_messages(task)
            observed: ObservedInteractions = self._transport.execute(
                target=target,
                protocol=protocol,
                messages=messages,
                timeout_ms=timeout_ms,
            )
        else:
            observed = ObservedInteractions(interactions=(), transport_errors=())

        expected_rules = _task_to_expected_rules(task)
        verification: VerificationResult = self._verification.verify_count_rules(
            expected=expected_rules,
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

        result: dict[str, object] = {
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
        if self._capture_replay and target:
            cap = self._capture_replay.write_capture(
                run_id=run_input.run_id,
                target_id=run_input.target_id,
                task_id=run_input.task_id,
                protocol=protocol,
                observed=observed,
            )
            if cap.get("ok"):
                result["capture_path"] = cap.get("path", "")
        return result

    def list_tasks(self) -> list[dict[str, object]]:
        """List registered tasks. Returns [] when no task registry is wired."""
        if self._task_registry is None:
            return []
        return self._task_registry.list_tasks()

    def load_task(self, path: str) -> dict[str, object]:
        """Load and register a task from path (runtime, without restart)."""
        if self._task_registry is None:
            return {"ok": False, "task_id": "", "error_code": "NO_REGISTRY"}
        return self._task_registry.register_from_path(path)

    def compose_task(self, base_task_ids: list[str], overrides: dict[str, object]) -> dict[str, object]:
        """Compose a new task from base tasks and register it (runtime, no restart)."""
        if self._task_registry is None:
            return {"ok": False, "task_id": "", "error_code": "NO_REGISTRY"}
        return self._task_registry.compose(base_task_ids, overrides)

    def create_task(self, definition: dict[str, object]) -> dict[str, object]:
        """Create and register a task from an in-memory definition (create from scratch)."""
        if self._task_registry is None:
            return {"ok": False, "task_id": "", "error_code": "NO_REGISTRY"}
        return self._task_registry.register_definition(definition)