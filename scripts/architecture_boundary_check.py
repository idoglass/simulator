#!/usr/bin/env python3
"""CI checks for architecture boundary and UI-thread safety rules."""

from __future__ import annotations

import argparse
import ast
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = ROOT / "src" / "simulator"

FRAMEWORK_MODULES = {"tkinter", "textual", "py_gui", "tk_mvc"}


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


def candidate_files(base_ref: str | None, head_ref: str | None) -> list[Path]:
    if base_ref and head_ref:
        files: list[Path] = []
        for rel in changed_files(base_ref, head_ref):
            p = ROOT / rel
            if not p.exists() or not p.is_file():
                continue
            if p.suffix != ".py":
                continue
            try:
                p.relative_to(SRC_ROOT)
            except ValueError:
                continue
            files.append(p)
        return sorted(files)

    if not SRC_ROOT.exists():
        return []
    return sorted(SRC_ROOT.rglob("*.py"))


def import_modules(tree: ast.AST) -> list[tuple[str, int]]:
    modules: list[tuple[str, int]] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                modules.append((alias.name, node.lineno))
        elif isinstance(node, ast.ImportFrom):
            prefix = "." * node.level
            module = f"{prefix}{node.module or ''}"
            modules.append((module, node.lineno))
    return modules


def segments(module: str) -> list[str]:
    normalized = module.lstrip(".")
    if not normalized:
        return []
    return [part for part in normalized.split(".") if part]


def path_kind(path: Path) -> tuple[bool, bool, bool, bool]:
    rel = path.relative_to(ROOT).as_posix()
    is_domain = "/domain/" in rel
    is_workflow = "/workflows/" in rel
    is_ui = "/adapters/ui/" in rel
    is_transport = "/adapters/transport/" in rel
    return is_domain, is_workflow, is_ui, is_transport


def has_time_sleep_call(tree: ast.AST) -> list[int]:
    lines: list[int] = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        func = node.func
        if (
            isinstance(func, ast.Attribute)
            and isinstance(func.value, ast.Name)
            and func.value.id == "time"
            and func.attr == "sleep"
        ):
            lines.append(node.lineno)
    return lines


def check_file(path: Path) -> list[str]:
    rel = path.relative_to(ROOT).as_posix()
    failures: list[str] = []

    try:
        src = path.read_text(encoding="utf-8")
        tree = ast.parse(src, filename=rel)
    except SyntaxError as exc:
        return [f"{rel}:{exc.lineno}: syntax error while parsing: {exc.msg}"]

    is_domain, is_workflow, is_ui, is_transport = path_kind(path)
    modules = import_modules(tree)

    for module, line in modules:
        parts = segments(module)
        top = parts[0] if parts else ""
        has_adapters = "adapters" in parts

        # Coupling guards for core layers.
        if is_domain or is_workflow:
            if has_adapters:
                failures.append(
                    f"{rel}:{line}: domain/workflow must not import adapter module '{module}'"
                )
            if top in FRAMEWORK_MODULES:
                failures.append(
                    f"{rel}:{line}: domain/workflow must not import UI framework module '{module}'"
                )
            if top == "socket":
                failures.append(
                    f"{rel}:{line}: domain/workflow must not import socket (transport concern)"
                )

        # UI adapter guards for transport/threading leakage.
        if is_ui:
            if has_adapters and "transport" in parts:
                failures.append(
                    f"{rel}:{line}: UI adapter must not import transport adapter '{module}'"
                )
            if top == "socket":
                failures.append(
                    f"{rel}:{line}: UI adapter must not import socket (blocking I/O risk on UI thread)"
                )

        # Transport adapter guards for reverse coupling.
        if is_transport:
            if has_adapters and "ui" in parts:
                failures.append(
                    f"{rel}:{line}: transport adapter must not import UI adapter '{module}'"
                )
            if top in FRAMEWORK_MODULES:
                failures.append(
                    f"{rel}:{line}: transport adapter must not import UI framework module '{module}'"
                )

    # Explicit UI-thread blocking anti-pattern in UI adapters.
    if is_ui:
        for line in has_time_sleep_call(tree):
            failures.append(f"{rel}:{line}: UI adapter must not call time.sleep()")

    return failures


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-ref")
    parser.add_argument("--head-ref")
    args = parser.parse_args()

    files = candidate_files(args.base_ref, args.head_ref)
    if not files:
        print("[ok] No Python files to check under src/simulator.")
        return 0

    failures: list[str] = []
    for path in files:
        failures.extend(check_file(path))

    if failures:
        for failure in failures:
            print(f"[fail] {failure}")
        print(f"\nBoundary check failed with {len(failures)} violation(s).")
        return 1

    print(f"[ok] Architecture boundary checks passed for {len(files)} file(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
