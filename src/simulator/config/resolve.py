"""Resolve config-backed catalog views for UI surfaces."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from simulator.config.contracts import list_contracts
from simulator.config.targets import list_targets, load_runtime_config
from simulator.config.tasks import list_tasks
from simulator.domain.ports import ConfigCatalogPort


@dataclass(frozen=True)
class RuntimeCatalogService(ConfigCatalogPort):
    """Simple catalog service for configuration-backed listings."""

    config_path: Path
    tasks_dir: Path

    def list_targets(self) -> list[dict[str, str]]:
        return list_targets(load_runtime_config(self.config_path))

    def list_contracts(self) -> list[dict[str, str]]:
        return list_contracts(load_runtime_config(self.config_path))

    def list_tasks(self) -> list[dict[str, str]]:
        return list_tasks(self.tasks_dir)

