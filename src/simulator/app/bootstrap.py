"""Bootstrap: wire dependencies and create runnable app. No UI/framework in domain."""

from __future__ import annotations

from pathlib import Path

from simulator.adapters.capture_replay import FileCaptureReplayAdapter
from simulator.adapters.events import InMemoryEventBus
from simulator.adapters.logging import ConsoleLoggingAdapter
from simulator.adapters.tasks import FileTaskRegistryAdapter
from simulator.adapters.transport import CompositeTransportAdapter
from simulator.adapters.verification import CountVerificationAdapter
from simulator.config.targets import get_default_targets, resolve_target
from simulator.domain.models.target_and_task import TargetRef
from simulator.domain.services import SimulationService
from simulator.workflows import RunWorkflow


def create_app(
    mode: str = "tui",
    tasks_dir: Path | None = None,
) -> dict[str, object]:
    """
    Create a runnable app container. Mode is 'gui' or 'tui'.
    Returns container with simulation_service, workflow, and mode for UI entry points.
    """
    logger = ConsoleLoggingAdapter()
    event_bus = InMemoryEventBus()
    verification = CountVerificationAdapter()
    transport = CompositeTransportAdapter()
    task_registry = FileTaskRegistryAdapter(tasks_dir=tasks_dir)
    targets = get_default_targets()

    def target_resolver(target_id: str) -> TargetRef | None:
        return resolve_target(target_id, targets)

    capture_replay = FileCaptureReplayAdapter()
    workflow = RunWorkflow(
        verification_port=verification,
        event_bus=event_bus,
        logger=logger,
        transport_port=transport,
        task_registry_port=task_registry,
        target_resolver=target_resolver,
        capture_replay_port=capture_replay,
    )
    simulation_service = SimulationService(workflow)

    return {
        "workflow": workflow,
        "simulation_service": simulation_service,
        "capture_replay": capture_replay,
        "mode": mode,
        "logger": logger,
    }
