# Port Contracts (Interfaces)

This document defines the core interface contracts (ports) used by domain/services.
Adapters implement these interfaces.

## Design Rules

1. Domain/workflow code depends only on these interfaces.
2. Adapters (`adapters/*`) implement the interfaces.
3. Interface methods return deterministic success/failure structures.
4. No UI/framework/network implementation detail leaks into interfaces.

---

## 1) Transport Port

**Purpose:** abstract TCP/UDP client+server message execution for simulation runs.

```python
class TransportPort(Protocol):
    def execute(
        self,
        *,
        target: "TargetRef",
        protocol: "ProtocolType",
        messages: list["MessageEnvelope"],
        timeout_ms: int,
    ) -> "ObservedInteractions": ...
```

**Behavior notes**
- Supports `protocol` = TCP or UDP.
- Used by run/replay workflows.
- Returns ordered observed interactions + transport-level errors.

**Plain-language explanation**
- The simulator core says "send these messages to this target over TCP/UDP."
- The transport adapter does the protocol work and returns what actually happened.

---

## 2) Contract Port

**Purpose:** load and validate `.h`/`ctypes` contract definitions.

```python
class ContractPort(Protocol):
    def load_sources(self, sources: list["ContractSource"]) -> "ContractBundle": ...
    def validate_message(self, message: "MessageEnvelope", bundle: "ContractBundle") -> "ValidationResult": ...
```

**Behavior notes**
- Accepts repository-managed and user-provided `.h` sources.
- Fails fast on unknown type/field references.
- Supports dual input entry types:
  - A: generated ctypes Python directory
  - B: raw `.h` directory
- Both entry types feed the same normalize+validate pipeline (`architecture/contract-mapping.md`).

**Plain-language explanation**
- This is the gatekeeper for message shapes.
- If a message does not match `.h`/`ctypes` rules, execution stops early.

---

## 3) Task Registry Port

**Purpose:** manage built-in/runtime tasks, lookup, and atomic registration.

```python
class TaskRegistryPort(Protocol):
    def register_atomic(self, definition: "TaskDefinition") -> "TaskRegisterResult": ...
    def get(self, task_id: str) -> "TaskDefinition | None": ...
    def list(self) -> list["TaskDefinitionSummary"]: ...
    def compose(self, base_task_ids: list[str], overrides: dict) -> "TaskDefinition": ...
```

**Behavior notes**
- Registration is atomic and deterministic.
- Duplicate/conflict behavior is explicit in return result.

**Plain-language explanation**
- This is the single source of truth for runnable tasks.
- A task is either fully registered or not registered at all.

---

## 4) Verification Port

**Purpose:** evaluate expected vs observed interactions.

```python
class VerificationPort(Protocol):
    def verify_count_rules(
        self,
        expected: list["ExpectedInteraction"],
        observed: "ObservedInteractions",
    ) -> "VerificationResult": ...
```

**Behavior notes**
- MVP semantics are count-based.
- Result includes pass/fail + mismatch details.

**Plain-language explanation**
- After a run, this checks whether expected interactions happened the expected number of times.
- It returns a clear pass/fail result plus mismatch details.

---

## 5) Capture/Replay Port

**Purpose:** file-based capture persistence and replay input loading.

```python
class CaptureReplayPort(Protocol):
    def write_capture(
        self,
        *,
        observed: "ObservedInteractions",
        metadata: "CaptureMetadata",
    ) -> "CaptureWriteResult": ...

    def read_capture(self, capture_path: str) -> "CaptureReadResult": ...
```

**Behavior notes**
- Capture artifacts are file-based in MVP.
- Metadata must include replay-critical fields (protocol, target, task/version context).

**Plain-language explanation**
- This writes captured run traffic to files and reads files back for replay.
- Replay uses saved metadata so behavior is repeatable.

---

## 6) Event Bus Port

**Purpose:** publish/subscribe domain/application events without hard coupling.

```python
class EventBusPort(Protocol):
    def publish(self, event: "DomainEvent") -> None: ...
    def subscribe(self, event_type: type["DomainEvent"], handler: "EventHandler") -> "SubscriptionRef": ...
```

**Behavior notes**
- Domain/services publish events; adapter implementations dispatch handlers.
- Default desktop implementation can be in-process.

**Plain-language explanation**
- Core modules emit events without knowing who listens.
- Subscribers react to events through a shared event bus contract.

---

## 7) Logging Port (Optional abstraction)

**Purpose:** standardize structured logging and redaction behavior.

```python
class LoggingPort(Protocol):
    def info(self, event: str, **fields) -> None: ...
    def warn(self, event: str, **fields) -> None: ...
    def error(self, event: str, **fields) -> None: ...
```

**Behavior notes**
- Fields include correlation keys (`run_id`, `task_id`, `target_id`).
- Sensitive values are redacted before emission.

**Plain-language explanation**
- This standardizes how services write logs.
- It ensures useful tracing fields are present and sensitive data is masked.

---

## 8) Mapping to Adapters

- `TransportPort` -> `adapters/transport/tcp`, `adapters/transport/udp`
- `ContractPort` -> `adapters/contracts`
- `TaskRegistryPort` -> `adapters/tasks`
- `VerificationPort` -> `adapters/verification`
- `CaptureReplayPort` -> `adapters/capture_replay`
- `EventBusPort` -> (app in-memory implementation and/or future `adapters/events`)

---

## Requirement Mapping

- GR-022, GR-023, GR-026, GR-027, GR-028, GR-029, GR-030, GR-031, GR-058
