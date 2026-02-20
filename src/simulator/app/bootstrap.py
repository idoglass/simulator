"""Bootstrap: wire dependencies and create runnable app. No UI/framework in domain."""

from __future__ import annotations

from simulator.adapters.events import InMemoryEventBus
from simulator.adapters.logging import ConsoleLoggingAdapter
from simulator.adapters.verification import CountVerificationAdapter
from simulator.workflows import RunWorkflow


def create_app(mode: str = "tui") -> dict[str, object]:
    """
    Create a runnable app container. Mode is 'gui' or 'tui'.
    Returns a container with workflow and mode for UI entry points to use.
    """
    logger = ConsoleLoggingAdapter()
    event_bus = InMemoryEventBus()
    verification = CountVerificationAdapter()
    workflow = RunWorkflow(
        verification_port=verification,
        event_bus=event_bus,
        logger=logger,
    )
    return {
        "workflow": workflow,
        "mode": mode,
        "logger": logger,
    }
