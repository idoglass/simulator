"""In-memory event bus. Implements EventBusPort for desktop single-process use."""

from __future__ import annotations

from typing import Any


class InMemoryEventBus:
    """Publish domain events. Subscribers can be added later; for foundation, publish is no-op."""

    def publish(self, event: dict[str, Any]) -> None:
        """Emit event. Handler registration not required for minimal run flow."""
        # Optional: dispatch to registered handlers by event_type
        pass
