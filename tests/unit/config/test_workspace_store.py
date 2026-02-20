"""Unit tests for workspace store (TKT-C02-02)."""

from __future__ import annotations

import tempfile
from pathlib import Path

from simulator.config.workspace_store import list_ids, load_json, save_json


def test_save_and_load_json() -> None:
    with tempfile.TemporaryDirectory() as d:
        root = Path(d)
        path = root / "sub" / "entity.json"
        save_json(path, {"id": "e1", "name": "E1"})
        assert path.exists()
        assert load_json(path) == {"id": "e1", "name": "E1"}


def test_load_json_missing_returns_none() -> None:
    with tempfile.TemporaryDirectory() as d:
        assert load_json(Path(d) / "missing.json") is None


def test_list_ids() -> None:
    with tempfile.TemporaryDirectory() as d:
        root = Path(d)
        (root / "a.json").write_text("{}")
        (root / "b.json").write_text("{}")
        assert set(list_ids(root)) == {"a", "b"}
