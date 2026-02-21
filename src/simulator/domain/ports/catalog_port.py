"""Domain port for listing simulator catalog resources."""

from __future__ import annotations

from typing import Protocol


class ConfigCatalogPort(Protocol):
    """Read-only catalog access for UI surfaces."""

    def list_targets(self) -> list[dict[str, str]]:
        """Return configured target summaries."""

    def list_contracts(self) -> list[dict[str, str]]:
        """Return configured contract summaries."""

    def list_tasks(self) -> list[dict[str, str]]:
        """Return registered/discoverable task summaries."""

