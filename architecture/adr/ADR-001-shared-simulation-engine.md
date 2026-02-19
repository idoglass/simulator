# ADR-001: Shared Simulation Engine for GUI and TUI

- Status: Accepted
- Date: 2026-02-19

## Context

The project must support both GUI and TUI while preserving consistent behavior and avoiding duplicated core logic.

## Decision

Use one shared simulation engine (domain/services + workflows) that both UI adapters call.

- GUI/TUI layers only map user interactions to engine operations.
- Business rules, transport orchestration, verification, and task execution remain in shared core modules.

## Consequences

Positive:

- Consistent behavior across GUI and TUI.
- Reduced duplication and lower maintenance overhead.
- Easier shared testing for run and verification flows.

Trade-offs:

- Stronger discipline needed to prevent framework-specific leakage into domain code.
- UI-specific edge cases require adapter translation rather than core branching.

## Alternatives Considered

1. Separate GUI and TUI cores (rejected): higher duplication and drift risk.
2. UI-first orchestration with thin shared helpers (rejected): weak architecture boundaries.

## Requirement Mapping

- GR-012, GR-026, GR-058
