"""Entry point: python -m simulator [--gui | --tui]. Desktop runtime mode."""

from __future__ import annotations

import argparse
import sys
from uuid import uuid4

from simulator.app.bootstrap import create_app


def _run_mvp_flow(container: dict[str, object]) -> None:
    """Run one simulation flow via shared simulation service (target + task)."""
    service = container["simulation_service"]
    run_id = f"run-{uuid4().hex[:8]}"
    result = service.run(
        run_id=run_id,
        target_id="default-target",
        task_id="ping-smoke",
        protocol="tcp",
    )
    assert result.get("run_id") == run_id
    assert "verification" in result
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
            from simulator.adapters.ui.gui.main import run_gui
            run_gui(container)
        except ImportError as e:
            print(f"[warn] GUI not available: {e}", file=sys.stderr)
            print("[info] Running one flow in CLI instead.", file=sys.stderr)
            _run_mvp_flow(container)
        return 0

    if args.tui:
        try:
            from simulator.adapters.ui.tui.main import run_tui
            run_tui(container)
        except ImportError:
            _run_mvp_flow(container)
        return 0

    _run_mvp_flow(container)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
