# DDS Core 03: Sequence Execution Engine

## 1. Purpose

Specify deterministic step orchestration for sequence runs, including retry, timeout, and failure-policy behavior.

## 2. Inputs and Outputs

Input:

- `sequence_id`
- run-time overrides (optional): timeout/retry/policy/scheduler toggles

Output:

- `RunSummary` with:
  - `run_id`
  - final status (`PASS`, `FAIL`, `COMPLETE_WITH_FAILURES`)
  - per-step records
  - error list
  - timing summary

## 3. Step Lifecycle

Each step transitions through:

`PENDING -> SENT -> VERIFIED` or `FAILED`

Optional transient states:

- `RETRYING`
- `SKIPPED` (disabled step or policy-induced skip)

## 4. Orchestration Algorithm

```text
start_run(sequence_id):
  bundle = resolve_and_validate(sequence_id)
  run_ctx = create_run_context(bundle)
  start_periodic_scheduler(run_ctx)

  for step in bundle.steps ordered by order_index:
    if step.disabled: record SKIPPED; continue
    result = execute_step(step, run_ctx)
    if result.failed and failure_policy == stop_on_fail:
      finalize FAIL
      stop scheduler
      return

  finalize PASS or COMPLETE_WITH_FAILURES
  stop scheduler
```

## 5. Step Execution Contract

`execute_step(step, run_ctx)` performs:

1. optional `delay_before_ms`
2. task resolution from registry
3. transport send via gateway
4. response collection window
5. verification rule evaluation
6. structured event emission

## 6. Retry and Timeout Policy

Defaults from SRS:

- step timeout: 5000 ms
- step retry_count: 0
- target retry_count: 1
- transport connect/read/write defaults handled by transport adapter

Retry precedence:

1. step-level explicit retry
2. fallback to target-level retry
3. no retries beyond configured bounds

## 7. Failure Policy Handling

- `stop_on_fail`: stop next steps, finalize `FAIL`
- `continue_on_fail`: continue remaining steps, finalize `COMPLETE_WITH_FAILURES` if any failure exists

## 8. Determinism Rules

- Foreground sequence order always follows `order_index`.
- Periodic task events may interleave in timeline, but cannot reorder step execution.
- Every step execution attempt includes deterministic attempt counter.
