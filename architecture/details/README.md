# Detailed Design Specification (DDS) Pack

This folder contains a design package derived from:

- `requirements/SRS_DRAFT.md` (v0.3.1)

It is intentionally split into:

- `core/` -> runtime-critical design details
- `supporting/` -> UI, validation, observability, and quality details

## Structure

### Core

1. `core/01-system-context-and-component-model.md`
2. `core/02-domain-data-model-and-storage.md`
3. `core/03-sequence-execution-engine.md`
4. `core/04-task-runtime-and-periodic-scheduler.md`
5. `core/05-transport-adapter-design.md`
6. `core/06-verification-engine-design.md`
7. `core/07-stateless-boundary-and-run-context.md`

### Supporting

1. `supporting/01-ui-design-gui-tui.md`
2. `supporting/02-validation-and-error-model.md`
3. `supporting/03-observability-and-nfr-design.md`
4. `supporting/04-test-traceability-and-quality-gates.md`

## Suggested Reading Order

1. Core 01 -> Core 07
2. Supporting 01 -> Supporting 04

## Coverage Intent

This DDS set covers all major SRS areas:

- Data schemas and constraints
- Sequence/task/periodic execution behavior
- Parallel scheduling model
- GUI/TUI parity and runtime controls
- Validation and concrete error-code handling
- Logging, NFR baseline, and test traceability
