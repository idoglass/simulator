# Verification Specification (MVP Count-Based)

This document defines the verification behavior for expected-vs-observed interactions.

## 1) Scope

- MVP verification is **count-based**.
- Verification runs after transport execution in normal runs and replay runs.
- Verification behavior is shared by both GUI and TUI through the same core engine.

## 2) Verification Inputs

Verification evaluates:

1. `expected_rules`: list of expected interaction rules.
2. `observed`: ordered observed interactions from transport/replay.
3. `context`: run/task/target correlation metadata.

### 2.1 Expected Rule Shape (MVP)

Each expected rule must include:

- `rule_id`: stable unique identifier in the run scope.
- `matcher`: fields used to select matching observed interactions.
- `expected_count`: integer `>= 0`.
- `comparison`: comparison operator for count assertion.

Optional fields:

- `description`
- `tags`

### 2.2 Matcher Fields (MVP)

MVP matcher supports:

- `direction`: `send` or `receive`
- `message_type`: canonical message type name
- `headers_contains`: key/value map (all listed pairs must match when present)
- `payload_fields_equals`: key/value map using canonical field paths
- `sequence_index_range`: optional inclusive index range over the observed list

### 2.3 Count Comparison Operators (MVP Baseline)

- Required baseline: `eq` (actual count must equal expected count).
- Optional extension point (post-MVP): `gte`, `lte`, `between`.

For architecture MVP acceptance, `eq` support is mandatory.

## 3) Observed Interaction Requirements

Observed interactions must be provided in deterministic order and include:

- `interaction_index` (monotonic within run)
- `timestamp`
- `direction`
- `message_type`
- `headers`
- `payload` (redaction-safe handling in logs/output views)
- correlation fields (`run_id`, `target_id`, `task_id` when available)

## 4) Evaluation Procedure (Deterministic)

For each expected rule, in declared rule order:

1. Validate rule shape (`rule_id`, `expected_count`, supported matcher fields).
2. Filter `observed` by matcher.
3. Apply `sequence_index_range` constraint when present.
4. Compute `actual_count` = number of matched observations.
5. Evaluate comparison (`eq` for MVP baseline).
6. Emit one `rule_result`.
7. If failed, emit one `mismatch` entry.

Overall verification output is deterministic for identical inputs.

## 5) Pass/Fail Conditions

A rule **passes** when:

- rule is valid, and
- count comparison evaluates true.

A rule **fails** when:

- count comparison evaluates false, or
- rule validation/evaluation fails.

Overall verification:

- `passed = true` only if all rules pass and no verification engine errors occur.
- `passed = false` if any rule fails or any verification engine error occurs.

## 6) Mismatch Reporting Format

Mismatch reporting must be structured and stable.

### 6.1 Verification Result Envelope

```json
{
  "run_id": "string",
  "target_id": "string",
  "task_id": "string",
  "passed": false,
  "summary": {
    "total_rules": 3,
    "passed_rules": 2,
    "failed_rules": 1
  },
  "rule_results": [],
  "mismatches": [],
  "generated_at": "ISO-8601 timestamp"
}
```

### 6.2 Rule Result Entry

Each `rule_result` should include:

- `rule_id`
- `passed`
- `expected_count`
- `actual_count`
- `comparison`
- `matched_interaction_indexes` (bounded list; truncate with count metadata if large)

### 6.3 Mismatch Entry

Each mismatch must include:

- `mismatch_id`
- `rule_id`
- `code` (one of `COUNT_MISMATCH`, `RULE_INVALID`, `MATCHER_EVALUATION_ERROR`)
- `message` (human-readable)
- `expected_count`
- `actual_count`
- `comparison`
- `matcher_snapshot`
- `sample_observed_indexes` (bounded sample for diagnostics)
- correlation fields (`run_id`, `target_id`, `task_id`)

Mismatch list order must follow expected rule declaration order.

## 7) UI and Logging Exposure Rules

1. GUI and TUI must display `passed` status, summary counts, and mismatch entries.
2. Full payload bodies should not be required for mismatch diagnosis in default UI views.
3. Logs should include correlation fields and rule IDs for traceability.
4. Sensitive data must be redacted in logs and user-facing views.

## 8) MVP Non-Goals

The following are out of scope for MVP verification:

- temporal assertions based on absolute time windows
- fuzzy/regex matching across arbitrary payload text
- protocol-stateful multi-step assertions beyond count-based matching
- probabilistic assertions

## 9) Architecture-Level Test Expectations

Minimum tests for verification behavior:

1. all rules pass with exact count matches
2. single-rule count mismatch produces failed result and one mismatch entry
3. multiple-rule mixed pass/fail with deterministic summary counts
4. `expected_count = 0` rule pass/fail behavior
5. invalid rule input produces `RULE_INVALID` mismatch deterministically
6. deterministic output ordering for repeated identical inputs

## 10) Requirement Mapping

- GR-030, GR-026, GR-039, GR-059

## Related Artifact

- `architecture/verification-roadmap.md`
