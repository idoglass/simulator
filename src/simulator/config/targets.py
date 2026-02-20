"""Target resolution from config. No UI/transport in config."""

from __future__ import annotations

from simulator.domain.models.target_and_task import TargetRef


# Multi-application capacity: max concurrent runs per process (configurable, validated)
DEFAULT_MAX_CONCURRENT_RUNS = 10


def get_default_targets() -> dict[str, TargetRef]:
    """Default targets for MVP smoke (localhost)."""
    return {
        "default-target": TargetRef(
            target_id="default-target",
            name="Default localhost",
            host="127.0.0.1",
            port=9999,
            protocol="tcp",
            mode="client",
        ),
        "default-udp": TargetRef(
            target_id="default-udp",
            name="Default UDP localhost",
            host="127.0.0.1",
            port=9998,
            protocol="udp",
            mode="client",
        ),
    }


def resolve_target(
    target_id: str, targets: dict[str, TargetRef] | None = None
) -> TargetRef | None:
    """Resolve TargetRef by target_id. Uses get_default_targets() if targets is None."""
    if targets is None:
        targets = get_default_targets()
    return targets.get(target_id)
