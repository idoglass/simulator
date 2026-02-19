#!/usr/bin/env python3
"""Smoke checks for GUI/TUI integration expectations."""

from __future__ import annotations

from pathlib import Path
import importlib
import sys

ROOT = Path(__file__).resolve().parents[1]


def must_exist(path: Path, failures: list[str]) -> None:
    if not path.exists():
        failures.append(f"Missing required path: {path.relative_to(ROOT)}")


def main() -> int:
    failures: list[str] = []

    py_gui = ROOT / "py-gui"
    general_req = ROOT / "requirements" / "GENERAL_REQUIREMENTS.md"
    feat_dir = ROOT / "requirements" / "feat"
    gitmodules = ROOT / ".gitmodules"

    must_exist(py_gui, failures)
    must_exist(general_req, failures)
    must_exist(feat_dir / "gui-and-tui-interfaces.md", failures)
    must_exist(feat_dir / "shared-simulation-engine-gui-tui.md", failures)
    must_exist(feat_dir / "mvc-architecture-framework-compliance.md", failures)
    must_exist(gitmodules, failures)

    if gitmodules.exists():
        text = gitmodules.read_text(encoding="utf-8")
        if "path = py-gui" not in text:
            failures.append("`.gitmodules` missing `path = py-gui` entry")

    if general_req.exists():
        req_text = general_req.read_text(encoding="utf-8")
        if "tk-mvc" not in req_text:
            failures.append("General requirements missing tk-mvc framework reference")
        if "Textual" not in req_text:
            failures.append("General requirements missing Textual framework reference")

    # GUI framework import smoke after CI installs submodule package.
    try:
        importlib.import_module("tk_mvc")
    except ModuleNotFoundError as exc:  # pragma: no cover - CI smoke only
        # In headless runners tkinter can be unavailable; don't block non-GUI checks.
        if exc.name == "tkinter":
            print("[warn] tkinter unavailable in runner; skipping tk_mvc import smoke.")
        else:
            failures.append(f"Unable to import tk_mvc package: {exc}")
    except Exception as exc:  # pragma: no cover - CI smoke only
        failures.append(f"Unable to import tk_mvc package: {exc}")

    if failures:
        for item in failures:
            print(f"[fail] {item}")
        print("\nGUI/TUI smoke check failed.")
        return 1

    print("GUI/TUI smoke check passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
