"""Bootstrap: wire dependencies and create runnable app. No UI/framework in domain."""

from __future__ import annotations

from pathlib import Path

from simulator.adapters.capture_replay import FileCaptureReplayAdapter
from simulator.adapters.events import InMemoryEventBus
from simulator.adapters.logging import ConsoleLoggingAdapter
from simulator.adapters.tasks import FileTaskRegistryAdapter
from simulator.adapters.tasks.file_task_registry import task_definition_to_dict
from simulator.adapters.transport import CompositeTransportAdapter
from simulator.adapters.transport.common.reachability import check_reachable
from simulator.adapters.verification import CountVerificationAdapter
from simulator.config.targets import get_default_targets, resolve_target
from simulator.domain.models.simulation_entities import ContractDefinition
from simulator.domain.models.target_and_task import TargetRef
from simulator.domain.services import SimulationService
from simulator.workflows import RunWorkflow


def create_app(
    mode: str = "tui",
    tasks_dir: Path | None = None,
) -> dict[str, object]:
    """
    Create a runnable app container. Mode is 'gui' or 'tui'.
    Returns container with simulation_service, workflow, targets CRUD, contracts CRUD, ping, and mode.
    """
    logger = ConsoleLoggingAdapter()
    event_bus = InMemoryEventBus()
    verification = CountVerificationAdapter()
    transport = CompositeTransportAdapter()
    task_registry = FileTaskRegistryAdapter(tasks_dir=tasks_dir)
    targets = dict(get_default_targets())
    contracts: dict[str, ContractDefinition] = {}

    def target_resolver(target_id: str) -> TargetRef | None:
        return resolve_target(target_id, targets)

    def list_targets() -> list[TargetRef]:
        return list(targets.values())

    def _to_ref(data: TargetRef | dict[str, object]) -> TargetRef:
        if isinstance(data, TargetRef):
            return data
        d = data
        return TargetRef(
            target_id=str(d.get("target_id", "")),
            name=str(d.get("name", "")),
            host=str(d.get("host", "127.0.0.1")),
            port=int(d.get("port", 9999)),
            protocol=str(d.get("protocol", "tcp")),
            mode=str(d.get("mode", "client")),
        )

    def add_target(ref: TargetRef | dict[str, object]) -> None:
        r = _to_ref(ref)
        targets[r.target_id] = r

    def update_target(old_id: str, new_ref: TargetRef | dict[str, object]) -> None:
        r = _to_ref(new_ref)
        if old_id != r.target_id:
            targets.pop(old_id, None)
        targets[r.target_id] = r

    def delete_target(target_id: str) -> None:
        targets.pop(target_id, None)

    def ping_target(target_id: str) -> dict[str, object]:
        t = targets.get(target_id)
        if t is None:
            return {"ok": False, "error": "Target not found"}
        return check_reachable(t)

    def _to_contract(data: ContractDefinition | dict[str, object]) -> ContractDefinition:
        if isinstance(data, ContractDefinition):
            return data
        d = data
        return ContractDefinition(
            contract_id=str(d.get("contract_id", "")),
            application_ref=str(d.get("application_ref", "default")),
            source_type=str(d.get("source_type", "user_h")),
            source_path=str(d.get("source_path", "")),
            version=str(d.get("version", "0.1.0")),
            checksum_sha256=str(d.get("checksum_sha256", "")),
        )

    def list_contracts() -> list[ContractDefinition]:
        return list(contracts.values())

    def add_contract(ref: ContractDefinition | dict[str, object]) -> None:
        c = _to_contract(ref)
        contracts[c.contract_id] = c

    def update_contract(old_id: str, new_ref: ContractDefinition | dict[str, object]) -> None:
        c = _to_contract(new_ref)
        if old_id != c.contract_id:
            contracts.pop(old_id, None)
        contracts[c.contract_id] = c

    def delete_contract(contract_id: str) -> None:
        contracts.pop(contract_id, None)

    def unregister_task(task_id: str) -> dict[str, object]:
        return task_registry.unregister(task_id)

    def get_task(task_id: str) -> dict[str, object] | None:
        t = task_registry.get(task_id)
        return task_definition_to_dict(t) if t else None

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
        "targets": targets,
        "list_targets": list_targets,
        "add_target": add_target,
        "update_target": update_target,
        "delete_target": delete_target,
        "ping_target": ping_target,
        "list_contracts": list_contracts,
        "add_contract": add_contract,
        "update_contract": update_contract,
        "delete_contract": delete_contract,
        "unregister_task": unregister_task,
        "get_task": get_task,
    }
