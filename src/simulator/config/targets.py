"""Target configuration helpers."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def load_runtime_config(path: Path | str) -> dict[str, Any]:
    """Load runtime JSON config from disk."""
    resolved = Path(path)
    with resolved.open("r", encoding="utf-8") as handle:
        payload = json.load(handle)
    if not isinstance(payload, dict):
        raise ValueError("Runtime config must be a JSON object.")
    return payload


def list_targets(config: dict[str, Any]) -> list[dict[str, str]]:
    """Extract target summaries in deterministic order."""
    rows = config.get("targets", [])
    if not isinstance(rows, list):
        return []

    results: list[dict[str, str]] = []
    for row in rows:
        if not isinstance(row, dict):
            continue
        target_id = str(row.get("target_id", "")).strip()
        if not target_id:
            continue
        name = str(row.get("name", target_id)).strip() or target_id
        results.append({"target_id": target_id, "name": name})
    return sorted(results, key=lambda item: item["target_id"])

