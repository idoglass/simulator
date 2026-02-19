# ADR-005: Transport Operations Run Off UI Thread

- Status: Accepted
- Date: 2026-02-19

## Context

Transport I/O includes blocking operations and timeout/retry waits that can freeze UI responsiveness if executed on GUI/TUI event loops.

## Decision

Execute transport operations in worker execution contexts (thread or async task), not on UI threads.

- UI updates must be marshaled back to the owning UI event loop.
- Cancellation is cooperative and closes sockets promptly.
- Event dispatch strategy should avoid deadlocks and long publisher stalls.

## Consequences

Positive:

- Preserves GUI/TUI responsiveness during transport-heavy runs.
- Better separation between user interaction and protocol operations.

Trade-offs:

- Additional concurrency complexity (synchronization, cancellation, ordering).
- Requires careful testing of race and lifecycle edges.

## Alternatives Considered

1. Single-threaded execution with non-blocking polling (rejected for MVP): higher complexity in UI loops and brittle responsiveness.
2. Dedicated process for transport (deferred): stronger isolation but higher operational complexity.

## Requirement Mapping

- GR-031, GR-026, GR-058, GR-059
