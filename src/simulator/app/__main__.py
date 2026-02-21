"""CLI entrypoint for simulator app."""

from __future__ import annotations

import argparse
from pathlib import Path
import sys

from simulator.adapters.ui.tui.main import render_listing
from simulator.app.container import build_container


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[3]


def build_parser() -> argparse.ArgumentParser:
    root = _repo_root()
    parser = argparse.ArgumentParser(prog="simulator")

    subparsers = parser.add_subparsers(dest="surface", required=True)
    tui = subparsers.add_parser("tui", help="TUI operations")

    tui_sub = tui.add_subparsers(dest="command", required=True)
    list_parser = tui_sub.add_parser("list", help="List catalog resources")
    list_parser.add_argument("resource", choices=["targets", "contracts", "tasks"])
    list_parser.add_argument(
        "--config",
        type=Path,
        default=root / "tests/fixtures/config/runtime-config.sample.json",
        help="Path to runtime config JSON.",
    )
    list_parser.add_argument(
        "--tasks-dir",
        type=Path,
        default=root / "tests/fixtures/tasks",
        help="Path containing task JSON files.",
    )

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.surface == "tui" and args.command == "list":
        container = build_container(config_path=args.config, tasks_dir=args.tasks_dir)
        print(render_listing(container.catalog, args.resource))
        return 0

    parser.print_help()
    return 2


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))

