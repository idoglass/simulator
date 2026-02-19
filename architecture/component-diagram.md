# Component Diagram

This document defines the high-level internal component layout and dependency directions.

## Component View (Mermaid)

```mermaid
flowchart TB
  subgraph UI["UI Adapters"]
    GUI["adapters/ui/gui <br/> (py-gui/tk-mvc integration)"]
    TUI["adapters/ui/tui <br/> (Textual integration)"]
  end

  subgraph Core["Core Application"]
    App["app/bootstrap + dependency container"]
    Workflows["workflows"]
    Domain["domain/services + domain/models"]
    Ports["domain/ports (interfaces)"]
  end

  subgraph Adapters["Boundary Adapters"]
    Transport["adapters/transport <br/> tcp + udp"]
    Contracts["adapters/contracts"]
    Tasks["adapters/tasks"]
    Verify["adapters/verification"]
    Replay["adapters/capture_replay"]
    Logging["logging"]
  end

  GUI --> Workflows
  TUI --> Workflows
  App --> Workflows
  Workflows --> Domain
  Domain --> Ports

  Transport --> Ports
  Contracts --> Ports
  Tasks --> Ports
  Verify --> Ports
  Replay --> Ports

  Workflows --> Logging
  Domain --> Logging
```

## Dependency Rules

1. `domain/*` depends only on `domain/ports/*` abstractions.
2. `adapters/*` implement port interfaces and depend on external frameworks/protocols.
3. `adapters/ui/*` and `adapters/transport/*` are grouped under `adapters/` by architectural role.
4. `workflows/*` orchestrate use cases and are the preferred entry point for UI adapters.
5. No direct dependency from domain to GUI/TUI/framework/network implementation code.

## Requirement Mapping

- GR-021, GR-026, GR-031, GR-038, GR-058
