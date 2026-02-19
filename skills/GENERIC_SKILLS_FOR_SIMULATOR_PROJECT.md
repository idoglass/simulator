# Generic Skills for a Stateless Simulator Project

## 1) Core Architecture Skill (MVC + Stateless Engine)

**Must demonstrate**
- Clear MVC separation: UI logic in views, orchestration in controllers, domain in models/services.
- Stateless request handling: no mutable per-session/per-target in-process state across requests.
- Shared engine for GUI and TUI paths.

**Good outcome**
- Same input produces same behavior through GUI or TUI.
- Core engine can be tested without UI dependencies.

**Common mistake**
- Business logic duplicated in GUI and TUI adapters.

---

## 2) Protocol and Transport Skill (TCP/UDP)

**Must demonstrate**
- Correct send/receive flow handling for TCP and UDP.
- Per-target transport configuration.
- Safe timeout/retry behavior and deterministic error reporting.

**Good outcome**
- Protocol-specific behavior isolated behind transport interfaces.

**Common mistake**
- Protocol branching spread across controllers/models instead of dedicated transport layer.

---

## 3) Message Contract Skill (`.h` / `ctypes`)

**Must demonstrate**
- Message structure validation driven only by `.h` / `ctypes` definitions.
- Rejection of unknown fields/types before runtime execution.
- Stable mapping between contract definitions and simulation runtime objects.

**Good outcome**
- Invalid contracts fail early with actionable diagnostics.

**Common mistake**
- Ad hoc custom parsing paths bypassing source contract definitions.

---

## 4) Task Engine Skill (Register, Compose, Runtime Load)

**Must demonstrate**
- Task registry with unique IDs and deterministic lifecycle.
- Runtime load/register before execution.
- Composition/extension from existing registered tasks.

**Good outcome**
- New behavior can be added without restart.

**Common mistake**
- Dynamic task loading bypasses validation and introduces inconsistent runtime states.

---

## 5) Matching and Verification Skill

**Must demonstrate**
- Configurable match rules (type/fields/sequence context).
- Verification assertions (count/order/content) with clear failure messages.
- Consistent verification reporting across GUI/TUI.

**Good outcome**
- Runs provide objective pass/fail interaction results.

**Common mistake**
- Weak "string contains" checks replacing structured matching.

---

## 6) Capture/Replay Skill

**Must demonstrate**
- Proxy/capture mode for message traffic.
- Replay mode with deterministic behavior under same input and task version.
- Capture metadata versioning (protocol, contract version, timestamp).

**Good outcome**
- Real traffic can seed repeatable simulation scenarios.

**Common mistake**
- Replay depends on hidden local state and becomes non-repeatable.

---

## 7) Observability Skill

**Must demonstrate**
- Verbose lifecycle logs (run start/stop, task load/register, send/receive, verification results).
- Runtime-configurable log levels.
- Sensitive-data redaction by default.

**Good outcome**
- Incidents can be diagnosed from logs without rerunning locally.

**Common mistake**
- Verbose logs without structure, redaction, or correlation IDs.

---

## 8) Quality Engineering Skill

**Must demonstrate**
- Unit/integration/e2e coverage for critical simulation paths.
- CI quality gates: lint, tests, security checks.
- Portability validation on target PC matrix.

**Good outcome**
- Changes to contracts/tasks/transports fail fast in CI when broken.

**Common mistake**
- Heavy manual testing with no regression harness for protocol/task behavior.

---

## 9) Documentation Skill

**Must demonstrate**
- GUI Help and TUI help/man updated for each user-facing capability.
- Feature docs mapped to baseline requirements IDs.
- Example-driven docs for common workflows (load task, run, verify, replay).

**Good outcome**
- New users can run core scenarios without source-code reading.

**Common mistake**
- Technical changes merged without user docs updates.
