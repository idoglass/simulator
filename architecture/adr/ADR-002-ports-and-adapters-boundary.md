# ADR-002: Ports-and-Adapters Boundary with Intentional `adapters/` Grouping

- Status: Accepted
- Date: 2026-02-19

## Context

The architecture must isolate external frameworks/protocols from domain logic, while supporting both UI and transport integrations.

## Decision

Adopt ports-and-adapters boundaries:

- Domain/workflows depend on abstract ports.
- Concrete integrations live under `adapters/`.
- `adapters/ui/*` and `adapters/transport/*` remain intentionally grouped by architectural role.

## Consequences

Positive:

- Strong dependency direction (`domain -> ports <- adapters`).
- Cleaner unit testing via port-level fakes.
- Easier replacement of external frameworks/protocol implementations.

Trade-offs:

- More abstraction layers and interface definitions to maintain.
- Requires strict code review discipline to avoid boundary violations.

## Alternatives Considered

1. Feature-folder structure mixing domain + adapters (rejected): higher coupling risk.
2. Framework-driven architecture centered on UI (rejected): weak domain isolation.

## Requirement Mapping

- GR-058, GR-044, GR-045
