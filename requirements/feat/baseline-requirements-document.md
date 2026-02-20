# FR-GR-001

- Source GR ID: GR-001
- Priority: P0
- Status: Implemented

## Feature Requirement
Keep an enforceable baseline requirements document in repository scope.

## Acceptance Criteria
- `requirements/GENERAL_REQUIREMENTS.md` exists and is used as baseline reference in feature specifications.

## Implementation
- **Enforcement:** `scripts/validate_requirements.py` (CI job `req-check` in `.github/workflows/pipeline.yml`):
  - Asserts `requirements/GENERAL_REQUIREMENTS.md` exists (FR-GR-001 baseline presence).
  - Asserts `requirements/feat/FEATURE_REQUIREMENTS_MASTER.md` references the baseline document by name.
  - Validates all feature docs under `requirements/feat/` include mapped GR IDs that exist in the baseline, ensuring feature specifications use the baseline as reference.
