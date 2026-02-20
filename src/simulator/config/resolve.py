"""Minimal config resolution. Layers: defaults -> project -> target -> run overrides."""

from __future__ import annotations


def merge_layers(*layers: dict[str, object]) -> dict[str, object]:
    """Shallow merge; later layers override earlier."""
    merged: dict[str, object] = {}
    for layer in layers:
        merged.update(layer)
    return merged


def resolve_run_config(
    *,
    defaults: dict[str, object],
    project_config: dict[str, object] | None = None,
    target_config: dict[str, object] | None = None,
    run_overrides: dict[str, object] | None = None,
) -> dict[str, object]:
    """Resolve config precedence. Generic; no coupling to one application model."""
    return merge_layers(
        defaults,
        project_config or {},
        target_config or {},
        run_overrides or {},
    )
