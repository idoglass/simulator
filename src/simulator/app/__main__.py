"""Entry point: python -m simulator [--gui | --tui]. Desktop runtime mode."""

from __future__ import annotations

import argparse
import sys
from uuid import uuid4

from simulator.app.bootstrap import create_app
from simulator.domain.models.run_models import RunInput


def _run_minimal_flow(container: dict[str, object]) -> None:
    """Run one minimal simulation flow to show core runs without app-model coupling."""
    workflow = container["workflow"]
    run_input = RunInput(
        run_id=f"run-{uuid4().hex[:8]}",
        target_id="default-target",
        task_id="default-task",
        protocol="tcp",
    )
    result = workflow.run(run_input)
    assert result.get("run_id") == run_input.run_id
    assert "verification" in result
    # Desktop flow executed; result can be shown by GUI/TUI.
    if container.get("mode") == "tui":
        print(f"[ok] Run completed: {result.get('verification', {}).get('summary', '')}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Simulator desktop application")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--gui", action="store_true", help="Launch GUI (Tkinter via py-gui)")
    group.add_argument("--tui", action="store_true", help="Launch TUI (Textual)")
    args = parser.parse_args()

    mode = "gui" if args.gui else "tui"
    container = create_app(mode=mode)

    if args.gui:
        try:
            # Defer GUI import so domain/workflow have no UI dependency
            from simulator.adapters.ui.gui.main import run_gui
            run_gui(container)
        except ImportError as e:
            print(f"[warn] GUI not available: {e}", file=sys.stderr)
            print("[info] Running one minimal flow in CLI instead.", file=sys.stderr)
            _run_minimal_flow(container)
        return 0

    # TUI or default: run minimal flow (full TUI app can be added later)
    _run_minimal_flow(container)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
