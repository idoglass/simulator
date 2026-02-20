# DDS Core 06: Verification Engine Design

## 1. Purpose

Define rule evaluation for expected responses, including count assertions and payload matching.

## 2. Inputs

- `ExpectedResponse` definition
- observed response set within assertion window
- message and contract metadata
- run/step context

## 3. Supported Rules (MVP)

- `exact`: observed payload must equal expected payload
- `subset`: expected fields must be present and equal
- `absent`: no response should be observed in assertion window

Assertion baseline:

- count-based assertion (`assertion_count`)

## 4. Evaluation Pipeline

1. Collect responses until `assertion_window_ms` elapsed.
2. Apply presence/absence pre-check.
3. Apply count assertion.
4. Apply payload rule (`exact`/`subset` when applicable).
5. Emit verdict and evidence.

## 5. Evidence Model

Verification result includes:

- `step_id`
- expected rule summary
- observed response summary
- count expected/actual
- mismatch fields (when applicable)
- final verdict (`PASS`/`FAIL`)
- mapped error code when failed

## 6. Failure Code Mapping

- no expected response observed -> `SRS-E-VER-001`
- count mismatch -> `SRS-E-VER-002`
- payload mismatch -> `SRS-E-VER-003`

## 7. Determinism and Ordering

- evaluation order is fixed: presence -> count -> payload
- result is deterministic for same observed set and same expectation definition
- periodic-task-produced responses use same verification logic as sequence steps
