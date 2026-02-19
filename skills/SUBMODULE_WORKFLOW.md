# Submodule Workflow (`py-gui`)

This document defines the standard workflow for updating and maintaining the `py-gui` submodule safely.

## Scope

- Main repo: `simulator`
- Submodule path: `py-gui`
- Submodule upstream: `https://github.com/idoglass/py-gui.git`

## Principles

1. Keep submodule updates **explicit and intentional**.
2. Update submodule pointer only with **compatibility validation**.
3. Avoid mixed changes: separate "submodule bump" commits from unrelated app logic.

## 1) First-Time Setup (clone + init)

```bash
git clone <simulator-repo-url>
cd simulator
git submodule update --init --recursive
```

## 2) Check Current Submodule State

```bash
git submodule status
git -C py-gui rev-parse --short HEAD
git -C py-gui branch --show-current
```

## 3) Update Submodule to Latest Upstream `main`

Use this when intentionally consuming newest framework changes.

```bash
git -C py-gui fetch origin
git -C py-gui checkout main
git -C py-gui pull origin main
git add py-gui
git commit -m "chore(submodule): bump py-gui to latest main"
```

## 4) Pin Submodule to a Specific Commit (preferred for stability)

Use this for deterministic builds/releases.

```bash
git -C py-gui fetch origin
git -C py-gui checkout <commit-sha>
git add py-gui
git commit -m "chore(submodule): pin py-gui to <commit-sha>"
```

## 5) Compatibility Validation Before Push

Run at minimum:

1. Simulator tests:
   - unit tests for major components
   - simple GUI and TUI e2e smoke
2. Cross-platform check intent:
   - Windows impact considered
   - Linux impact considered
3. Integration checks:
   - GUI still uses shared domain/service engine
   - TUI behavior unchanged for equivalent core flows

Recommended commands (adapt per repo tooling):

```bash
# from simulator repo root
pytest -q
```

```bash
# optional: validate submodule's own tests/docs baseline
pytest -q -c py-gui/pyproject.toml
```

## 6) Rollback Submodule Bump

If integration fails:

```bash
# restore previous pointer in simulator repo
git checkout HEAD~1 -- py-gui
git add py-gui
git commit -m "revert(submodule): rollback py-gui pointer"
```

Or reset to a known good SHA:

```bash
git -C py-gui checkout <known-good-sha>
git add py-gui
git commit -m "chore(submodule): set py-gui to known good <sha>"
```

## 7) PR / Review Requirements for Submodule Changes

Any PR that changes `py-gui` pointer MUST include:

- Why bump/pin is needed
- Old SHA -> New SHA
- Framework changes consumed (short summary)
- Compatibility validation results (unit/e2e + OS impact notes)
- Any follow-up migration work in simulator

### PR Notes Template

```text
Submodule update: py-gui
Old SHA: <old-sha>
New SHA: <new-sha>
Reason: <why update is needed>
Framework change summary:
- ...
- ...

Validation performed:
- Simulator unit tests: PASS/FAIL
- GUI smoke: PASS/FAIL
- TUI smoke: PASS/FAIL
- Windows impact reviewed: YES/NO
- Linux impact reviewed: YES/NO

Follow-up actions:
- ...
```

## 8) Anti-Patterns (Do Not Do)

- Do not update submodule pointer accidentally as part of unrelated refactors.
- Do not merge submodule bumps without compatibility notes.
- Do not modify framework code in detached state without upstream traceability.
- Do not bypass review when GUI framework changes affect shared engine behavior.
