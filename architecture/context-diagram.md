# Context Diagram

This document defines the system context for the simulator and its external boundaries.

## Scope

- Runtime: desktop application
- GUI stack: `py-gui` submodule (`tk-mvc`)
- TUI stack: Textual
- Transport scope (MVP): TCP + UDP (client/server)

## Context (Mermaid)

```mermaid
flowchart LR
  User[Operator / Developer]
  GUI[GUI App <br/> (Tkinter via py-gui/tk-mvc)]
  TUI[TUI App <br/> (Textual)]
  Sim[Simulator Core <br/> (domain + workflows + ports)]
  HFiles[.h Contract Files <br/> (repo-managed or user-provided)]
  TaskFiles[Task Definition Files]
  CaptureFiles[Capture / Replay Files]
  Net[External Targets / Applications <br/> over TCP/UDP]
  Logs[Logs / Local Console]

  User --> GUI
  User --> TUI
  GUI --> Sim
  TUI --> Sim
  HFiles --> Sim
  TaskFiles --> Sim
  Sim --> CaptureFiles
  CaptureFiles --> Sim
  Sim --> Net
  Net --> Sim
  Sim --> Logs
```

## Boundary Notes

1. GUI and TUI are separate interaction surfaces but call one shared simulation core.
2. `.h` files and task files are external inputs into core validation/execution flow.
3. Network targets are external systems; simulator interacts via transport adapters.
4. Capture/replay artifacts are file-based in MVP.

## Requirement Mapping

- GR-011, GR-012, GR-019, GR-022, GR-023, GR-029, GR-031, GR-058
