#!/usr/bin/env python3
"""Shared CI test runner for Linux and Windows jobs."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def run(cmd: list[str], allow_fail: bool = False) -> int:
    print(f"[run] {' '.join(cmd)}")
    cp = subprocess.run(cmd, cwd=ROOT, text=True)
    if cp.returncode != 0 and not allow_fail:
        print(f"[fail] Command failed with code {cp.returncode}")
    return cp.returncode


def has_tests(path: Path) -> bool:
    if not path.exists() or not path.is_dir():
        return False
    return any(path.rglob("test_*.py")) or any(path.rglob("*_test.py"))


def tkinter_runtime_available() -> bool:
    """Return True if tkinter can be imported and root window can initialize."""
    try:
        import tkinter as tk  # noqa: PLC0415

        root = tk.Tk()
        root.withdraw()
        root.destroy()
        return True
    except Exception as exc:  # pragma: no cover - runtime/environment dependent
        print(f"[warn] tkinter runtime not available for GUI tests: {exc}")
        return False


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--skip-submodule-tests", action="store_true")
    args = parser.parse_args()

    failures = 0

    # Basic syntax smoke for Python sources.
    failures += run([sys.executable, "-m", "compileall", "-q", "requirements", "skills", "scripts"])

    root_tests = ROOT / "tests"
    if has_tests(root_tests):
        failures += run([sys.executable, "-m", "pytest", "-q", str(root_tests)])
    else:
        print("[info] No root tests discovered; skipping root pytest.")

    submodule_tests = ROOT / "py-gui" / "tests"
    if (
        not args.skip_submodule_tests
        and has_tests(submodule_tests)
        and tkinter_runtime_available()
    ):
        failures += run([sys.executable, "-m", "pytest", "-q", str(submodule_tests)])
    else:
        print("[info] Submodule GUI tests skipped (disabled, missing tests, or no tkinter runtime).")

    if failures:
        print(f"[fail] CI test runner found {failures} failure(s).")
        return 1
    print("[ok] CI test runner passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
