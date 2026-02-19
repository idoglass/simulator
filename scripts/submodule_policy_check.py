#!/usr/bin/env python3
"""Submodule policy checks for pull requests."""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GITMODULES = ROOT / ".gitmodules"


def run(cmd: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(cmd, cwd=ROOT, text=True, capture_output=True, check=False)


def changed_files(base_ref: str, head_ref: str) -> list[str]:
    cp = run(["git", "diff", "--name-only", f"{base_ref}...{head_ref}"])
    if cp.returncode != 0:
        cp = run(["git", "diff", "--name-only", base_ref, head_ref])
    if cp.returncode != 0:
        print(f"[warn] unable to compute diff: {cp.stderr.strip()}")
        return []
    return [line.strip() for line in cp.stdout.splitlines() if line.strip()]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-ref", required=True)
    parser.add_argument("--head-ref", required=True)
    parser.add_argument("--pr-body", default="")
    args = parser.parse_args()

    files = changed_files(args.base_ref, args.head_ref)
    if not files:
        print("No changed files detected for submodule policy check.")
        return 0

    py_gui_changed = any(f == "py-gui" or f.startswith("py-gui/") for f in files)
    if not py_gui_changed:
        print("No py-gui submodule change detected. Policy check passed.")
        return 0

    failures: list[str] = []

    if not GITMODULES.exists():
        failures.append(".gitmodules missing while py-gui changed")
    else:
        text = GITMODULES.read_text(encoding="utf-8")
        if 'path = py-gui' not in text:
            failures.append("`.gitmodules` missing `path = py-gui`")
        if "https://github.com/idoglass/py-gui.git" not in text:
            failures.append("`.gitmodules` missing expected py-gui URL")

    body = args.pr_body or ""
    if not re.search(r"Old SHA\s*:", body, flags=re.IGNORECASE):
        failures.append("PR body missing 'Old SHA:' in submodule update notes")
    if not re.search(r"New SHA\s*:", body, flags=re.IGNORECASE):
        failures.append("PR body missing 'New SHA:' in submodule update notes")
    if not re.search(r"Reason\s*:", body, flags=re.IGNORECASE):
        failures.append("PR body missing 'Reason:' in submodule update notes")

    if failures:
        for failure in failures:
            print(f"[fail] {failure}")
        print("\nSubmodule policy check failed.")
        return 1

    print("Submodule policy check passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
