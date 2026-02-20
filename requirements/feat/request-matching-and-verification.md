# FR-GR-030

- Source GR ID: GR-030
- Priority: P0
- Status: Implemented

## Feature Requirement
Support request/message matching rules and verification assertions for expected interactions, with count-based verification in MVP.

## Acceptance Criteria
- Simulator supports configurable match rules (for example message type, header/field values, and sequence context).
- Simulator can assert expected interactions occurred using count-based verification in MVP, with pass/fail results available during or after a run.
- Verification results are exposed in both GUI and TUI with pass/fail status and mismatch details.

## Implementation
- **CountVerificationAdapter** implements count-based rules (expected_count, comparison eq/ge). Run workflow builds expected rules from task steps (expect blocks) and calls verify_count_rules(expected, observed). Result includes passed, summary, mismatches; returned in run result and available to GUI/TUI.
