"""JSON workspace storage for entity persistence (TKT-C02-02)."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def load_json(path: Path) -> dict[str, Any] | None:
    """Load one JSON file; return None if missing."""
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text())
    except (json.JSONDecodeError, OSError):
        return None


def save_json(path: Path, data: dict[str, Any]) -> None:
    """Write JSON file; parent dir created if needed."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2))


def list_ids(dir_path: Path, suffix: str = ".json") -> list[str]:
    """List entity IDs from filenames (e.g. app_id.json -> app_id)."""
    if not dir_path.exists():
        return []
    return [p.stem for p in dir_path.glob(f"*{suffix}") if p.is_file()]
