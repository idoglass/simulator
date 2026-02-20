# Verification Extension Roadmap (Post-MVP)

This document defines the planned evolution of verification beyond MVP count-based assertions.

## 1) Current Baseline (MVP)

Current behavior is defined in `architecture/verification-spec.md`:

- deterministic matcher evaluation
- count-based assertions (`eq`)
- structured mismatch reporting

## 2) Roadmap Goals

1. Support richer protocol correctness checks without breaking MVP behavior.
2. Keep verification deterministic and debuggable.
3. Roll out advanced assertions in bounded phases with test gates.

## 3) Phase Plan

## Phase V2: Ordered Sequence Assertions

Scope:

- ordered message expectations (A before B)
- contiguous subsequence matching
- optional strict mode (no extra matched events in sequence window)

New rule capabilities:

- `sequence`: ordered list of matcher steps
- `ordered`: boolean
- `allow_gaps`: boolean

Success criteria:

- deterministic pass/fail for identical inputs
- mismatch includes first divergence index and expected step

## Phase V3: Stateful Assertions

Scope:

- correlate request/response pairs by keys
- assert transitions across interaction state machine
- session-scoped invariants (within run boundary)

New rule capabilities:

- `correlation_keys`
- `state_machine_ref`
- `transition_assertions`

Success criteria:

- state transition violations produce stable error codes
- correlation failures point to missing/duplicate partner interactions

## Phase V4: Temporal and Window Assertions

Scope:

- relative timing assertions (e.g., response within N ms)
- bounded window checks over interaction streams

New rule capabilities:

- `max_latency_ms`
- `window_size`
- `window_slide`

Success criteria:

- deterministic timing evaluation under controlled timestamps
- clear tolerance policy documented and testable

## 4) Backward Compatibility Rules

1. MVP count-based rules remain fully supported.
2. New rule features are additive; existing schemas continue to parse.
3. Unsupported rule capabilities fail fast with explicit code.
4. Major schema changes require version bump and migration guidance.

## 5) Error Code Extension Plan

Extend verification error family with stable codes, for example:

- `VERIFICATION_SEQUENCE_MISMATCH`
- `VERIFICATION_STATE_TRANSITION_INVALID`
- `VERIFICATION_CORRELATION_MISSING`
- `VERIFICATION_TEMPORAL_WINDOW_FAILED`
- `VERIFICATION_FEATURE_UNSUPPORTED`

Codes should be added to `architecture/error-codes.md` when implemented.

## 6) Test Strategy Evolution

For each phase, required tests include:

1. happy path pass case
2. deterministic mismatch case
3. malformed rule validation failure
4. repeated identical input determinism check
5. mixed-rule compatibility with legacy count-based assertions

## 7) Rollout and Safety Gates

1. Feature flags for new assertion families during early rollout.
2. Per-phase documentation update (spec + examples + migration notes).
3. CI gate addition before enabling by default.
4. Explicit ADR if semantics or compatibility model changes materially.

## 8) Requirement Mapping

- GR-030, GR-039, GR-040
