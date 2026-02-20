# DDS Core 01: System Context and Component Model

## 1. Purpose

Define the runtime component model that satisfies SRS v0.3.1 for:

- message send/receive simulation
- response verification
- multi-application support
- periodic parallel task execution
- GUI/TUI shared engine behavior

## 2. Design Drivers (SRS)

- SRS-FR-005, SRS-FR-006, SRS-FR-007: deterministic sequence execution and verification
- SRS-FR-013: GUI/TUI parity through a shared engine
- SRS-FR-017..SRS-FR-019: periodic/continuous tasks with ON/OFF controls
- SRS-FR-020: stateless execution boundary

## 3. Context Boundary

Inside system boundary:

- Configuration Model Service
- Sequence Execution Engine
- Periodic Task Scheduler
- Verification Engine
- Transport Adapter Layer (TCP/UDP)
- Run Context and Event Stream

Outside system boundary:

- Remote target endpoints
- User-provided `.h` contracts
- Runtime-loaded task plugins

## 4. Logical Components

1. **AppConfigService**
   - Owns CRUD for app/target/contract/task/transport/message/sequence entities.
   - Performs reference integrity checks before persisting.

2. **ExecutionOrchestrator**
   - Builds run plan from selected sequence.
   - Coordinates step execution order and failure policy handling.

3. **TaskRegistry**
   - Resolves built-in and runtime-loaded tasks.
   - Rejects unregistered task usage.

4. **PeriodicScheduler**
   - Executes periodic tasks independently of sequence step order.
   - Enforces overlap policy (`skip`, `queue`, `parallel`).

5. **TransportGateway**
   - Provides protocol/mode abstraction for TCP/UDP client/server.
   - Applies timeout and endpoint validation rules.

6. **VerificationService**
   - Applies rule set (`exact`, `subset`, `absent` + count assertion).
   - Emits step-level PASS/FAIL result records.

7. **RunEventBus**
   - Publishes lifecycle events to GUI/TUI observers and logger.
   - Carries correlation IDs and run IDs.

8. **RunStateFactory**
   - Creates isolated per-run mutable state.
   - Guarantees no mutable carryover between runs.

## 5. Component Interaction (Happy Path)

1. UI selects sequence -> `ExecutionOrchestrator.start(sequence_id)`.
2. Orchestrator requests immutable definitions from `AppConfigService`.
3. Orchestrator creates new run context from `RunStateFactory`.
4. Orchestrator starts `PeriodicScheduler` for enabled periodic tasks.
5. For each ordered step:
   - resolve task via `TaskRegistry`
   - send via `TransportGateway`
   - verify via `VerificationService`
   - publish event via `RunEventBus`
6. Apply failure policy and complete run.
7. Stop scheduler for this run context.

## 6. Key Design Constraints

- UI layers never call transport directly; all calls flow through orchestrator/services.
- Periodic scheduler cannot block foreground sequence loop.
- Only validated `.h`/`ctypes` bindings may reach send path.
- Every error must include code/category/run context metadata.
