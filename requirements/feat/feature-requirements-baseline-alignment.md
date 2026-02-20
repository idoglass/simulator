# FR-GR-002

- Source GR ID: GR-002
- Priority: P0
- Status: Implemented

## Feature Requirement
Enforce that each feature requirement document aligns to baseline rules.

## Acceptance Criteria
- Every feature requirements document includes mapped GR IDs and no unapproved conflicts with baseline requirements.

## Implementation
- **Enforcement:** `scripts/validate_requirements.py` (CI job `req-check`):
  - Each feature doc under `requirements/feat/*.md` (except index, master, template, example) must include `Source GR ID:` referencing a GR ID that exists in `requirements/GENERAL_REQUIREMENTS.md`.
  - Each feature doc must contain sections `## Feature Requirement` and `## Acceptance Criteria`.
  - On PRs, changed feature docs are re-validated with the same rules (FR-GR-002-prefixed failures).
  - Unapproved conflicts are detected when a doc references a GR ID not in the baseline; substantive conflict review remains in approval process.
