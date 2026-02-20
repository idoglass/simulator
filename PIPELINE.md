# Development Pipeline

This project uses a gated feature-delivery pipeline so each implementation satisfies requirements, quality, and documentation expectations.

## Pipeline Stages

1. **Requirement Gate**
   - Update feature requirement docs under `requirements/feat/`.
   - Ensure mapping to GR IDs and acceptance criteria.
   - CI job: `req-check`.

2. **Implementation Gate**
   - Implement with shared engine parity across GUI (`py-gui`/`tk-mvc`) and TUI (Textual).
   - Respect MVC boundaries and stateless execution rules.

3. **Architecture Boundary Gate**
   - Enforce import/layering boundaries and UI-thread safety checks.
   - CI job: `architecture-boundary-guard`.

4. **Quality Gate**
   - Run unit tests for major components + simple e2e.
   - CI jobs:
     - `lint-test-linux`
     - `lint-test-windows`
     - `gui-tui-smoke`

5. **Submodule Policy Gate**
   - If `py-gui` pointer changes, include Old SHA / New SHA / Reason in PR.
   - Follow `skills/SUBMODULE_WORKFLOW.md`.
   - CI job: `submodule-policy-check`.

6. **Documentation & Traceability Gate**
   - Update docs/help as needed.
   - Keep `requirements/feat/INDEX.md` status aligned (`Planned`, `In Progress`, `Done`).

## CI Files and Scripts

- Workflow:
  - `.github/workflows/pipeline.yml`
- PR template:
  - `.github/pull_request_template.md`
- Validation scripts:
  - `scripts/validate_requirements.py`
  - `scripts/architecture_boundary_check.py`
  - `scripts/ci_test_runner.py`
  - `scripts/gui_tui_smoke_check.py`
  - `scripts/submodule_policy_check.py`

## Local Pre-PR Commands

```bash
python scripts/validate_requirements.py
python scripts/architecture_boundary_check.py
python scripts/ci_test_runner.py
python scripts/gui_tui_smoke_check.py
```

## Required Skills References

- `skills/PROJECT_SKILLS_STANDARD_V1.md`
- `skills/CODE_SMELL_AND_OOP_CHECKLIST.md`
- `skills/SUBMODULE_WORKFLOW.md`
