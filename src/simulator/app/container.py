"""Application dependency container."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from simulator.config.resolve import RuntimeCatalogService
from simulator.domain.ports import ConfigCatalogPort


@dataclass(frozen=True)
class AppContainer:
    """Container for app-wide service dependencies."""

    catalog: ConfigCatalogPort


def build_container(*, config_path: Path, tasks_dir: Path) -> AppContainer:
    """Build and return a deterministic application container."""
    return AppContainer(catalog=RuntimeCatalogService(config_path=config_path, tasks_dir=tasks_dir))

