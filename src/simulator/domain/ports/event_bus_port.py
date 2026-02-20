"""Event bus port. Adapters implement publish/subscribe for domain events."""

from __future__ import annotations

from typing import Any, Protocol


class EventBusPort(Protocol):
    """Publish domain events without hard coupling to handlers."""

    def publish(self, event: dict[str, Any]) -> None: ...
