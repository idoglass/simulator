from __future__ import annotations

from pathlib import Path
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from simulator.adapters.ui.tui.main import render_listing  # noqa: E402
from simulator.app.container import build_container  # noqa: E402


class TestTuiListings(unittest.TestCase):
    def setUp(self) -> None:
        self.config_path = ROOT / "tests" / "fixtures" / "config" / "runtime-config.sample.json"
        self.tasks_dir = ROOT / "tests" / "fixtures" / "tasks"
        self.container = build_container(config_path=self.config_path, tasks_dir=self.tasks_dir)

    def test_tui_can_list_targets(self) -> None:
        output = render_listing(self.container.catalog, "targets")
        self.assertIn("target_id", output)
        self.assertIn("target-a", output)
        self.assertIn("Target A", output)

    def test_tui_can_list_contracts(self) -> None:
        output = render_listing(self.container.catalog, "contracts")
        self.assertIn("source_ref", output)
        self.assertIn("tests/fixtures/contracts/raw", output)
        self.assertIn("h_dir", output)

    def test_tui_can_list_tasks(self) -> None:
        output = render_listing(self.container.catalog, "tasks")
        self.assertIn("task_id", output)
        self.assertIn("ping-smoke", output)
        self.assertIn("Ping Smoke Task", output)


if __name__ == "__main__":
    unittest.main()

