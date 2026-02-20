"""File-backed repository implementations with reference integrity (TKT-C02-02)."""

from __future__ import annotations

from pathlib import Path

from simulator.config.workspace_store import load_json, list_ids, save_json
from simulator.domain.models.simulation_entities import (
    SimulatedApplication,
    TargetDefinition,
    TaskDefinitionSRS,
)


class FileApplicationRepository:
    def __init__(self, workspace_root: Path) -> None:
        self._dir = workspace_root / "applications"

    def get(self, app_id: str) -> SimulatedApplication | None:
        data = load_json(self._dir / f"{app_id}.json")
        if not data:
            return None
        return SimulatedApplication(
            app_id=data["app_id"],
            app_name=data["app_name"],
            description=data.get("description", ""),
            enabled=data.get("enabled", True),
        )

    def list_all(self) -> list[SimulatedApplication]:
        return [a for aid in list_ids(self._dir) if (a := self.get(aid))]

    def save(self, entity: SimulatedApplication) -> None:
        save_json(
            self._dir / f"{entity.app_id}.json",
            {
                "app_id": entity.app_id,
                "app_name": entity.app_name,
                "description": entity.description,
                "enabled": entity.enabled,
            },
        )

    def delete(self, app_id: str) -> None:
        path = self._dir / f"{app_id}.json"
        if path.exists():
            path.unlink()


class FileTargetRepository:
    def __init__(self, workspace_root: Path, app_repo: FileApplicationRepository) -> None:
        self._dir = workspace_root / "targets"
        self._app_repo = app_repo

    def get(self, target_id: str) -> TargetDefinition | None:
        data = load_json(self._dir / f"{target_id}.json")
        if not data:
            return None
        return TargetDefinition(
            target_id=data["target_id"],
            target_name=data["target_name"],
            application_ref=data["application_ref"],
            transport_ref=data["transport_ref"],
            timeout_ms=data.get("timeout_ms", 5000),
            retry_count=data.get("retry_count", 1),
        )

    def list_all(self) -> list[TargetDefinition]:
        return [t for tid in list_ids(self._dir) if (t := self.get(tid))]

    def save(self, entity: TargetDefinition) -> None:
        if self._app_repo.get(entity.application_ref) is None:
            raise ValueError("application_ref must reference existing app")
        save_json(
            self._dir / f"{entity.target_id}.json",
            {
                "target_id": entity.target_id,
                "target_name": entity.target_name,
                "application_ref": entity.application_ref,
                "transport_ref": entity.transport_ref,
                "timeout_ms": entity.timeout_ms,
                "retry_count": entity.retry_count,
            },
        )

    def delete(self, target_id: str) -> None:
        path = self._dir / f"{target_id}.json"
        if path.exists():
            path.unlink()


class FileTaskRepository:
    def __init__(self, workspace_root: Path, app_repo: FileApplicationRepository) -> None:
        self._dir = workspace_root / "tasks"
        self._app_repo = app_repo

    def get(self, task_id: str) -> TaskDefinitionSRS | None:
        data = load_json(self._dir / f"{task_id}.json")
        if not data:
            return None
        return TaskDefinitionSRS(
            task_id=data["task_id"],
            application_ref=data["application_ref"],
            task_name=data["task_name"],
            registration_type=data["registration_type"],
            task_ref=data["task_ref"],
            execution_mode=data.get("execution_mode", "oneshot"),
            periodic_config=data.get("periodic_config"),
        )

    def list_all(self) -> list[TaskDefinitionSRS]:
        return [t for tid in list_ids(self._dir) if (t := self.get(tid))]

    def save(self, entity: TaskDefinitionSRS) -> None:
        if self._app_repo.get(entity.application_ref) is None:
            raise ValueError("application_ref must reference existing app")
        save_json(
            self._dir / f"{entity.task_id}.json",
            {
                "task_id": entity.task_id,
                "application_ref": entity.application_ref,
                "task_name": entity.task_name,
                "registration_type": entity.registration_type,
                "task_ref": entity.task_ref,
                "execution_mode": entity.execution_mode,
                "periodic_config": entity.periodic_config or {},
            },
        )

    def delete(self, task_id: str) -> None:
        path = self._dir / f"{task_id}.json"
        if path.exists():
            path.unlink()
