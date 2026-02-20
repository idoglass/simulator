"""App container: single entrypoint for dependency wiring and service graph resolution.

SRS-FR-013, SRS-FR-020, SRS-NFR-003. GUI and TUI resolve the same shared service graph.
"""

from __future__ import annotations

from pathlib import Path

from simulator.app.bootstrap import create_app


class Container:
    """Composes orchestrator, scheduler, transport, verification, and repositories through one entrypoint."""

    def __init__(self, mode: str = "tui", tasks_dir: Path | None = None) -> None:
        self._app = create_app(mode=mode, tasks_dir=tasks_dir)

    def get_workflow(self):
        """Resolve run workflow (orchestrator)."""
        return self._app["workflow"]

    def get_simulation_service(self):
        """Resolve shared simulation service; GUI and TUI use this for parity."""
        return self._app["simulation_service"]

    def get_logger(self):
        """Resolve logging adapter."""
        return self._app["logger"]

    def get_capture_replay(self):
        """Resolve capture/replay adapter."""
        return self._app.get("capture_replay")

    def get_mode(self) -> str:
        """Current UI mode (gui | tui)."""
        return self._app.get("mode", "tui")
