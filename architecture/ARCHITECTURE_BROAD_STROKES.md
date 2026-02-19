# Architecture Plan (Broad Strokes)

This document defines a high-level architecture direction for the simulator project.
It is intentionally broad and should be refined into detailed design artifacts before implementation.

## 1) Architecture Principles

1. **Single shared simulation core** for both GUI and TUI.
2. **Strict separation of concerns**:
   - UI layers only handle interaction/rendering.
   - Domain/services handle business logic.
   - Adapters handle transport, file I/O, framework integration.
3. **Stateless run execution boundary** at application layer.
4. **Contract-driven behavior** from `.h` / `ctypes` definitions.
5. **Task-driven execution** via registered tasks only.
6. **Framework-aware, framework-contained** integration (`py-gui` for Tkinter MVC, Textual for TUI).

## 2) Main Components (High Level)

### A. Composition Root / App Bootstrap
- Loads config
- Wires dependencies
- Initializes logging and registries
- Starts GUI or TUI mode

### B. Shared Simulation Engine (Domain Services)
- Run orchestration (`start/stop/status`)
- Message flow execution
- Task dispatch and lifecycle
- Verification hooks

### C. Contract Subsystem
- `.h` source loading (repo-managed and user-provided files)
- `ctypes` model mapping
- Contract validation for message structures/fields

### D. Task Subsystem
- Task registry (built-in + runtime-loaded)
- Task validation + atomic registration
- Task composition/extension

### E. Transport Subsystem
- TCP adapter (client/server)
- UDP adapter (client/server)
- Per-target transport selection

### F. Verification and Matching
- Matching rules
- MVP count-based assertions
- Standardized pass/fail reporting

### G. Capture/Replay Subsystem
- File-based traffic capture
- Replay runner from capture artifacts
- Deterministic replay context metadata

### H. UI Adapters
- **GUI Adapter:** via `py-gui` (`tk-mvc`) integration
- **TUI Adapter:** via Textual
- Both call the same shared simulation engine APIs

### I. Observability
- Structured verbose logs with redaction
- Correlation IDs for runs/tasks/targets

## 3) Broad Runtime Flow

1. User starts app in GUI or TUI mode.
2. App loads contracts (`.h` -> `ctypes`) and tasks.
3. User selects target + protocol + scenario/task.
4. Shared engine executes run via selected transport adapter.
5. Matching/verification evaluates interactions.
6. Optional capture file is written and later replayed.
7. Results and logs are shown consistently in GUI/TUI.

## 4) Proposed File Structure (Target Shape)

```text
simulator/
  .github/
    workflows/
      pipeline.yml
  architecture/
    ARCHITECTURE_BROAD_STROKES.md
  requirements/
    GENERAL_REQUIREMENTS.md
    feat/
      INDEX.md
      ...
  skills/
    PROJECT_SKILLS_STANDARD_V1.md
    SUBMODULE_WORKFLOW.md
    ...
  py-gui/                         # submodule (tk-mvc framework)
  src/
    simulator/
      app/
        bootstrap.py
        dependency_container.py
      domain/
        models/
        services/
        ports/                    # abstract interfaces
      adapters/
        ui/
          gui/                    # tk-mvc integration glue only
          tui/                    # Textual integration glue only
        transport/
          tcp/
          udp/
        contracts/
        tasks/
        verification/
        capture_replay/
      workflows/
      config/
      logging/
  tests/
    unit/
    integration/
    e2e/
      gui/
      tui/
  scripts/
    validate_requirements.py
    ci_test_runner.py
    gui_tui_smoke_check.py
    submodule_policy_check.py
```

## 5) Requirements-to-Architecture Alignment (Broad)

- **GR-012, GR-026, GR-058:** Dual UI + framework compliance + shared engine.
- **GR-021:** Stateless boundary in domain/services.
- **GR-022, GR-009:** Contract subsystem enforces `.h` / `ctypes`.
- **GR-023, GR-027, GR-028:** Task registry/load/compose pipeline.
- **GR-031:** TCP/UDP client+server transport adapters.
- **GR-030:** Matching and count-based verification.
- **GR-029:** File-based capture/replay path.
- **GR-039, GR-040:** Unit + simple e2e + CI quality gates.

## 6) Best-Practice Guardrails

- No domain/service import from GUI/TUI modules.
- No duplicated core logic between GUI and TUI.
- Protocol branching isolated in transport adapters.
- Submodule (`py-gui`) updates follow `skills/SUBMODULE_WORKFLOW.md`.
- Every feature implementation updates requirement mapping and tests.

## 7) Next Detailed Artifacts (Before Coding)

1. Context diagram (external actors + boundaries)
2. Component diagram (engine/adapters/subsystems)
3. Data/contract flow diagram (`.h` -> `ctypes` -> runtime models)
4. Sequence diagram for one run (target + protocol + task + verify)
5. Risk register and mitigation plan
6. ADRs for key decisions (shared engine boundary, transport abstraction, task format)
