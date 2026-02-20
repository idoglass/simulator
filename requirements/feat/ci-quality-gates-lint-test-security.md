# FR-GR-040

- Source GR ID: GR-040
- Priority: P0
- Status: Implemented

## Feature Requirement
Enforce CI/CD gates for lint, tests, and security checks.

## Acceptance Criteria
- CI fails when lint, test, or security check stages fail.

## Implementation
- Pipeline: req-check (validate_requirements), architecture-boundary-guard, lint-test (Linux/Windows), gui-tui-smoke, submodule-policy. Security: pip-audit step added in lint-test-linux job.
