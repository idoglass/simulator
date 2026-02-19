# OOP, Code Smell, and Best-Practice Checklist

Use this checklist in design reviews and pull requests.

## A) OOP and Design Quality

- [ ] **Single Responsibility**: each class/module has one clear reason to change.
- [ ] **Open/Closed**: new protocols/tasks added via extension points, not broad switch edits.
- [ ] **Liskov Substitution**: protocol/task implementations are behaviorally interchangeable through interfaces.
- [ ] **Interface Segregation**: no oversized interfaces forcing irrelevant methods.
- [ ] **Dependency Inversion**: core engine depends on abstractions (transport/task providers), not concrete UI/network classes.
- [ ] **Explicit boundaries**: MVC layers are respected; controllers do not own protocol parsing logic.
- [ ] **Stateless core**: no hidden mutable state retained between independent runs.

## B) High-Risk Code Smells

- [ ] **God class/service** in simulation engine.
- [ ] **Shotgun surgery** when adding a protocol/task requires edits in many unrelated files.
- [ ] **Duplicated business logic** across GUI and TUI.
- [ ] **Primitive obsession** for message payloads instead of typed contract objects.
- [ ] **Long method / nested conditionals** in matching/verification.
- [ ] **Feature envy** where classes overreach into others' internals.
- [ ] **Inconsistent error handling** (exceptions in one path, return codes in another).
- [ ] **No deterministic IDs/correlation** in logs and run artifacts.
- [ ] **Submodule drift**: framework changed locally without clear upstream trace and pointer update rationale.

## C) Best Practices for This Project Type

- [ ] Keep `py-gui` framework integration traceable via submodule commit updates.
- [ ] Validate `.h` / `ctypes` contracts before task registration.
- [ ] Reject unknown message fields/types early with actionable errors.
- [ ] Keep task registry operations atomic (no partial registration on failure).
- [ ] Keep protocol behavior isolated per transport adapter (TCP/UDP).
- [ ] Include request matching and verification outputs in both GUI and TUI.
- [ ] Make capture/replay reproducible via versioned metadata.
- [ ] Redact sensitive fields in logs by default.
- [ ] Keep feature docs and help/man content updated in same change set.

## D) PR Review Quick Gate (Fail if any true)

- [ ] New behavior added without tests for core path.
- [ ] GUI and TUI behavior diverges for equivalent input.
- [ ] Logging added without redaction consideration.
- [ ] Runtime-loaded tasks bypass validation.
- [ ] New dependency added without reliability/license/security rationale.
- [ ] `py-gui` submodule changed without explicit reason and compatibility note.
