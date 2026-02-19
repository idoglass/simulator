# Integration Interface Inventory (APIs, Events, Files)

This document inventories architecture integration interfaces used by the simulator.

## 1) Port Interfaces (Internal API Contracts)

| Interface | Direction | Purpose | Defined In |
| --- | --- | --- | --- |
| `TransportPort.execute(...)` | Domain -> Adapter | Execute protocol transport for run/replay | `architecture/port-contracts.md` |
| `ContractPort.load_sources(...)` / `validate_message(...)` | Domain -> Adapter | Load and validate contract definitions | `architecture/port-contracts.md` |
| `TaskRegistryPort.register_atomic/get/list/compose` | Domain -> Adapter | Runtime task management | `architecture/port-contracts.md` |
| `VerificationPort.verify_count_rules(...)` | Domain -> Adapter | Expected-vs-observed verification | `architecture/port-contracts.md` |
| `CaptureReplayPort.write_capture/read_capture` | Domain -> Adapter | File capture/replay persistence | `architecture/port-contracts.md` |
| `EventBusPort.publish/subscribe` | Domain -> App/Adapter | Decoupled event dispatch | `architecture/port-contracts.md` |
| `LoggingPort.info/warn/error` | Domain -> Adapter | Structured logs with redaction | `architecture/port-contracts.md` |

## 2) Event Interfaces

| Event Group | Examples | Source Artifact |
| --- | --- | --- |
| Run lifecycle | `RunStarted`, `RunCompleted`, `RunFailed` | `architecture/event-model.md` |
| Task lifecycle | `TaskLoadRequested`, `TaskRegistered` | `architecture/event-model.md` |
| Verification | `VerificationStarted`, `VerificationFailed` | `architecture/event-model.md` |
| Capture/Replay | `CaptureWritten`, `ReplayCompleted` | `architecture/event-model.md` |

## 3) File Interfaces

| File Type | Direction | Purpose | Notes |
| --- | --- | --- | --- |
| `.h` directories | Input | Contract source ingestion | local and/or pinned remote snapshot |
| generated `ctypes` directories | Input | Alternate contract source ingestion | normalized through same pipeline |
| `.task.json` files | Input | Runtime task definitions | schema-versioned JSON |
| capture files (`.json`) | Output/Input | Capture and replay artifacts | includes replay-critical metadata |
| config files (`.json`/project-defined) | Input | Runtime configuration and compatibility data | normalized to `ResolvedRunConfig` |
| structured log files | Output | Diagnostics/traceability | redaction mandatory |

## 4) UI Boundary Interfaces

| Boundary | Inputs | Outputs |
| --- | --- | --- |
| GUI (`py-gui`/Tkinter MVC) | user run/capture/replay commands, task/config selections | status updates, verification summaries, diagnostics |
| TUI (Textual) | user run/capture/replay commands, task/config selections | status updates, verification summaries, diagnostics |

Both UI boundaries call the same run/capture/replay workflows in the shared engine.

## 5) External Runtime Interfaces

| Interface | Type | Notes |
| --- | --- | --- |
| TCP sockets | network I/O | client and server modes |
| UDP sockets | network I/O | client and server modes |
| Local filesystem | file I/O | config/task/capture/log artifacts |

## 6) Requirement Mapping

- GR-044, GR-045, GR-026, GR-031, GR-059
