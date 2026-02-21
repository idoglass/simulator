"""Task discovery helpers."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def _safe_load_json(path: Path) -> dict[str, Any] | None:
    try:
        with path.open("r", encoding="utf-8") as handle:
            payload = json.load(handle)
        if isinstance(payload, dict):
            return payload
    except (OSError, json.JSONDecodeError):
        return None
    return None


def list_tasks(tasks_dir: Path | str) -> list[dict[str, str]]:
    """List task definitions by loading task JSON files."""
    base = Path(tasks_dir)
    if not base.exists() or not base.is_dir():
        return []

    results: list[dict[str, str]] = []
    for file_path in sorted(base.glob("*.json")):
        payload = _safe_load_json(file_path)
        if not payload:
            continue
        task_id = str(payload.get("task_id", "")).strip()
        if not task_id:
            continue
        task_name = str(payload.get("name", task_id)).strip() or task_id
        results.append(
            {
                "task_id": task_id,
                "name": task_name,
                "source_file": str(file_path.name),
            }
        )
    return sorted(results, key=lambda item: item["task_id"])

