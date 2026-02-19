# Project Skills Standard v1 (Python Desktop Simulator)

This standard is tailored to current project decisions in `PROJECT_DISCOVERY_ANSWERS.md`.

## 1) Stack Baseline

- Language: **Python**
- GUI: **Tkinter-based MVC framework** (repo reference pending)
- TUI: **Textual**
- Runtime: **Desktop only**
- Protocols in MVP: **TCP + UDP** (client + server)
- TLS in MVP: **Out of scope**
- Verification in MVP: **Count-based**
- Capture/replay in MVP: **File-based**
- OS targets in MVP: **Windows + Linux**

## 2) Architecture and OOP Rules (Mandatory)

1. **Shared domain engine**  
   GUI and TUI SHALL call the same simulation service layer (no duplicated business logic).

2. **MVC boundaries**  
   - View: rendering and user input only  
   - Controller: orchestration and use-case wiring  
   - Model/Service: domain logic, protocol handling, task execution

3. **Stateless execution boundary**  
   No hidden mutable per-session/per-target state between independent runs.

4. **Dependency direction**  
   UI modules SHALL depend on service interfaces; service/domain SHALL NOT import UI modules.

5. **Extension-first protocol/task design**  
   New protocols/tasks should be added via adapters/registries, not switch-heavy edits across many files.

6. **Python typing discipline**  
   Public interfaces and domain models SHOULD use type hints; `Protocol`/ABC for transport and registry contracts.

## 3) Python Implementation Best Practices

- Keep Tkinter operations on the UI thread; run blocking network/file operations off the UI thread.
- Keep Textual command/view logic thin; delegate domain behavior to shared services.
- Normalize error model (typed exceptions or structured error objects, not mixed styles).
- Use structured logs with correlation IDs (`run_id`, `task_id`, `target_id`).
- Redact sensitive values by default in logs and captured artifacts.

## 4) Protocol and Message Rules

- MVP transport support SHALL include:
  - TCP send/receive (client and server behavior)
  - UDP send/receive (client and server behavior)
- Protocol selection SHALL be explicit per run/target configuration.
- Message contracts SHALL be validated against `.h`/`ctypes` definitions before execution.

## 5) Task, Matching, and Replay Rules

- Runtime task loading SHALL validate input before registration.
- Task registration SHALL be atomic (no partial state on failure).
- Verification SHALL support count-based assertions in MVP.
- Capture/replay SHALL be file-based and reproducible for the same input/task version context.

## 6) Code Smell Rejection List (Blocker)

Changes SHOULD be rejected if they introduce:

- Duplicated simulation logic in both GUI and TUI layers
- "God service" that combines transport, parsing, matching, and UI orchestration
- Cross-layer imports (domain importing UI code)
- Protocol-specific branches scattered through controllers/views
- Runtime task loading path that bypasses validation
- Logging without redaction consideration

## 7) Testing and Quality Gates

Minimum quality bar:

1. Unit tests for all major components:
   - transport adapters (TCP/UDP)
   - contract validation (`.h`/`ctypes`)
   - task registry/load/compose flows
   - matching/count verification
2. Simple e2e scenarios:
   - GUI path core run
   - TUI path core run
3. CI gates:
   - lint
   - tests
   - security/dependency checks

## 8) MVP Review Checklist (Use in PRs)

- [ ] Change preserves shared engine parity across GUI and TUI.
- [ ] MVC boundaries are respected.
- [ ] TCP/UDP behavior is covered by tests when touched.
- [ ] `.h`/`ctypes` contract validation path is preserved.
- [ ] Task loading remains validated and atomic.
- [ ] Count-based verification behavior is tested.
- [ ] Capture/replay file workflow (if touched) remains deterministic.
- [ ] Logging remains verbose + redacted.
- [ ] Windows and Linux impact considered.

## 9) Pending Decisions

- Final GUI framework reference repository details.
- Task definition format selection (JSON/YAML/other).
