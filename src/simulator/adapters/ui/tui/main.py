"""TUI listing utilities for simulator catalog entities."""

from __future__ import annotations

from simulator.domain.ports import ConfigCatalogPort


def _format_table(rows: list[dict[str, str]], columns: list[str]) -> str:
    if not rows:
        return ""
    header = " | ".join(columns)
    separator = "-+-".join("-" * len(col) for col in columns)
    lines = [header, separator]
    for row in rows:
        lines.append(" | ".join(row.get(col, "") for col in columns))
    return "\n".join(lines)


def render_targets(catalog: ConfigCatalogPort) -> str:
    rows = catalog.list_targets()
    if not rows:
        return "No targets found."
    return _format_table(rows, ["target_id", "name"])


def render_contracts(catalog: ConfigCatalogPort) -> str:
    rows = catalog.list_contracts()
    if not rows:
        return "No contracts found."
    return _format_table(rows, ["target_id", "source_ref", "entry_type"])


def render_tasks(catalog: ConfigCatalogPort) -> str:
    rows = catalog.list_tasks()
    if not rows:
        return "No tasks found."
    return _format_table(rows, ["task_id", "name", "source_file"])


def render_listing(catalog: ConfigCatalogPort, resource: str) -> str:
    """Render one of: targets, contracts, tasks."""
    if resource == "targets":
        return render_targets(catalog)
    if resource == "contracts":
        return render_contracts(catalog)
    if resource == "tasks":
        return render_tasks(catalog)
    raise ValueError(f"Unsupported resource listing: {resource}")

