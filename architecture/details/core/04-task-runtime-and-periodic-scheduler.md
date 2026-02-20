# DDS Core 04: Task Runtime and Periodic Scheduler

## 1. Purpose

Define how periodic tasks run continuously in parallel with sequence execution, and how ON/OFF controls are applied at runtime.

## 2. Scheduler Responsibilities

- discover enabled periodic tasks for active run context
- trigger executions at `interval_ms`
- apply overlap policy (`skip`, `queue`, `parallel`)
- enforce `max_parallel_runs` when applicable
- expose runtime status (`enabled`, `last_run_at`, `next_run_at`, failure streak)

## 3. Runtime Toggle Contract

UI command:

- `set_periodic_enabled(task_id, enabled: bool)`

Behavior:

- ON: scheduler starts task loop immediately or on next interval tick
- OFF: no new iterations start; in-flight iteration may finish

## 4. Concurrency Model

Suggested implementation:

- one scheduler supervisor per run context
- per periodic task worker loop
- bounded worker pool for `parallel` overlap mode

Foreground sequence loop and scheduler loops are independent cooperative workloads.

## 5. Overlap Policy Semantics

- `skip`
  - if prior execution is still active at tick time, drop this tick
  - emit warning event (`SRS-E-RUN-002`)
- `queue`
  - allow one pending trigger while one execution is active
  - additional ticks are dropped (`SRS-E-RUN-003`)
- `parallel`
  - allow concurrent executions up to `max_parallel_runs`
  - if limit reached, behavior degrades to `queue` with one pending slot

## 6. Scheduler Loop Pseudocode

```text
while run_ctx.active and periodic.enabled:
  wait(interval_ms with optional jitter)
  if not periodic.enabled: break
  apply_overlap_policy_and_dispatch(task_ref)
  update(next_run_at)
```

## 7. Failure Handling

- periodic execution failure does not automatically fail foreground sequence
- record `consecutive_failures` and last error
- optional policy hook can auto-disable task after threshold (future extension)

## 8. State Model

`PeriodicTaskRuntime` is created per run:

- `runtime_id`
- `task_ref`
- `enabled`
- `interval_ms`
- `last_run_at`
- `next_run_at`
- `run_count`
- `consecutive_failures`

This state is never persisted across independent runs.
