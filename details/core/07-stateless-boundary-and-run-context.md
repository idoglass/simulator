# DDS Core 07: Stateless Boundary and Run Context

## 1. Purpose

Enforce SRS stateless execution boundary while allowing persisted configuration artifacts.

## 2. Statelessness Contract

Must persist:

- configuration definitions (apps, targets, contracts, tasks, transports, messages, expectations, sequences)

Must not persist across independent runs:

- in-flight step statuses
- scheduler counters and runtime toggles
- transient transport session state
- temporary verification buffers

## 3. Run Context Model

Run context is created at start and destroyed at completion:

- `run_id`
- selected `sequence_id`
- start/end timestamps
- immutable resolved run bundle
- mutable step state map
- periodic runtime state map
- event stream cursor

## 4. Isolation Rules

1. New run gets a new `run_id` and fresh mutable containers.
2. No mutable object from prior run is reused by reference.
3. Runtime toggles (periodic ON/OFF) are scoped to active run context.
4. On run end, scheduler and workers are terminated before context disposal.

## 5. Restart and Recovery

- On process restart, only persisted configuration is reloaded.
- In-progress runs are not resumed unless an explicit future recovery feature is added.

## 6. Validation Scenario Link

SRS test alignment:

- SRS-TEST-015 validates no mutable leakage between run A and run B.
