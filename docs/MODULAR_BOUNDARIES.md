# Modular code ownership boundaries (FR-GR-038)

Modules and interfaces have clear ownership; cross-module dependencies are controlled.

## Ownership
- **domain/models, domain/ports, domain/services** – Core logic and contracts. No UI, no transport implementation.
- **workflows** – Use-case orchestration. Depends only on domain and ports.
- **adapters/ui** – GUI and TUI. Depends on simulation service/workflow; no transport or domain internals.
- **adapters/transport** – TCP/UDP. Implements TransportPort only.
- **adapters/tasks, adapters/verification, adapters/contracts, adapters/capture_replay** – Implement respective ports.
- **config** – Resolution and targets. No UI/transport.

## Enforcement
- CI `scripts/architecture_boundary_check.py` rejects domain/workflow imports of adapters, UI frameworks, socket.
- UI adapters must not import transport adapters.
