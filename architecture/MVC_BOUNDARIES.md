# MVC and Adapter Boundaries (FR-GR-058)

Feature design maps to MVC layers; adapter boundary is explicit and documented.

## Layer Ownership

| Layer | Location | Responsibility |
| --- | --- | --- |
| **Model / Domain** | `domain/models`, `domain/services` | Business entities and rules; no UI or transport code |
| **Ports (interfaces)** | `domain/ports` | Abstract contracts only; no framework/socket imports |
| **Workflows** | `workflows` | Use-case orchestration; call domain and ports only |
| **View/Controller** | `adapters/ui/gui`, `adapters/ui/tui` | Framework-specific UI; translate user actions to engine calls |
| **Transport** | `adapters/transport/tcp`, `adapters/transport/udp` | Protocol send/receive; implement TransportPort |

## Adapter Boundary Grouping

- **`adapters/ui`** – GUI (py-gui/tk-mvc) and TUI (Textual). Grouped by architectural role: both translate user intent into shared simulation engine API calls.
- **`adapters/transport`** – TCP and UDP. Grouped by role: both implement TransportPort for network I/O.

These are intentional boundary groupings, not shared implementation. Cross-import between `adapters/ui` and `adapters/transport` is forbidden (enforced by CI `architecture_boundary_check.py`).

## Review Gate

CI rejects:
- Domain or workflow importing `adapters/*`, UI frameworks, or `socket`
- UI adapter importing transport adapter or socket
- Transport adapter importing UI adapter or UI frameworks

Requirement mapping: GR-058.
