"""Config scaffolding template."""

from __future__ import annotations


def merge_layers(*layers: dict[str, object]) -> dict[str, object]:
    """Shallow merge helper: later layers override earlier ones."""
    merged: dict[str, object] = {}
    for layer in layers:
        merged.update(layer)
    return merged


def resolve_run_config(
    *,
    defaults: dict[str, object],
    project_config: dict[str, object],
    target_config: dict[str, object],
    run_overrides: dict[str, object],
) -> dict[str, object]:
    """Apply precedence: defaults -> project -> target -> run overrides."""
    return merge_layers(defaults, project_config, target_config, run_overrides)


def validate_transport_config(transport: dict[str, object]) -> list[str]:
    """Return deterministic validation errors (empty list on success)."""
    errors: list[str] = []
    if transport.get("protocol") not in {"tcp", "udp"}:
        errors.append("CONFIG_PROTOCOL_INVALID")
    mode = transport.get("mode")
    if mode not in {"client", "server"}:
        errors.append("CONFIG_SCHEMA_INVALID")
    port = transport.get("port")
    if not isinstance(port, int) or port < 1 or port > 65535:
        errors.append("CONFIG_PORT_INVALID")
    return errors

