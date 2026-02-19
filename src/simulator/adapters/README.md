# Adapters Boundary (Intentional)

This directory groups modules by **architectural role**, not by shared implementation.

`adapters/` contains components that translate between external systems/frameworks and the shared simulator core.

## Why `ui` and `transport` are both here

- `ui/` adapters translate user interactions (GUI/TUI) into core engine calls.
- `transport/` adapters translate protocol I/O (TCP/UDP) into core engine contracts.

They do not need to share code to belong together here.  
They are grouped because both are **boundary adapters** around the same domain core.

## Boundary rules

1. Adapters may depend on domain/service interfaces (ports).
2. Domain/services MUST NOT depend on adapter implementation modules.
3. Shared business logic belongs in domain/services, not in adapters.
