# Implementation Tickets from DDS (SRS v0.3.1)

This backlog is derived from:

- `architecture/details/core/*.md`
- `architecture/details/supporting/*.md`
- `requirements/SRS_DRAFT.md`

All tickets are intentionally small but complete.

## Global Requirement Consideration (applies to every ticket)

Each ticket MUST explicitly consider the full requirement set, not only its primary scope.

- Full functional set: `SRS-FR-001..SRS-FR-021`
- Full UI set: `SRS-UI-001..SRS-UI-008`
- Full NFR set: `SRS-NFR-001..SRS-NFR-008`
- Error model: `SRS-E-VAL-*`, `SRS-E-TASK-*`, `SRS-E-TRN-*`, `SRS-E-VER-*`, `SRS-E-RUN-*`, `SRS-E-INT-*`
- Traceability/tests: SRS Section 13 + Section 14

Mandatory done checks for every ticket:

1. Map changed code to primary SRS IDs and verify no regressions against all remaining SRS IDs.
2. Add or update tests for affected behavior.
3. Preserve stateless boundary and structured error envelope.
4. Update traceability references when behavior or tests change.

---

## A) Tickets from `core/01-system-context-and-component-model.md`

### TKT-C01-01 - Create app container and service wiring skeleton
- Primary SRS: `SRS-FR-013`, `SRS-FR-020`, `SRS-NFR-003`
- Requirement consideration: **Global Requirement Consideration** above
- Scope: Add dependency wiring for orchestrator, scheduler, transport, verification, repositories.
- Relevant files:
  - `architecture/details/core/01-system-context-and-component-model.md`
  - `requirements/SRS_DRAFT.md`
  - `src/simulator/app/bootstrap.py` (new)
  - `src/simulator/app/container.py` (new)
  - `src/simulator/workflows/execution_orchestrator.py` (new)
  - `tests/unit/app/test_container.py` (new)
- Done when:
  - Services are composed through one container entrypoint.
  - GUI and TUI can resolve the same shared service graph.
- **Status:** Complete
- **Completed:** `container.py`, `execution_orchestrator.py`, `tests/unit/app/test_container.py` added; GUI/TUI use same graph via `Container`.

### TKT-C01-02 - Implement run event bus contract
- Primary SRS: `SRS-FR-014`, `SRS-FR-015`, `SRS-UI-002`
- Requirement consideration: **Global Requirement Consideration** above
- Scope: Add event bus interfaces/events for run lifecycle and step events.
- Relevant files:
  - `architecture/details/core/01-system-context-and-component-model.md`
  - `src/simulator/domain/ports/event_bus_port.py` (new)
  - `src/simulator/domain/services/run_event_bus.py` (new)
  - `src/simulator/domain/models/run_events.py` (new)
  - `tests/unit/domain/test_run_event_bus.py` (new)
- Done when:
  - Run/step/scheduler events are publishable and observable by UI + logging adapters.
- **Status:** Complete
- **Completed:** `run_events.py`, `run_event_bus.py`, `tests/unit/domain/test_run_event_bus.py`; EventBusPort exists.

---

## B) Tickets from `core/02-domain-data-model-and-storage.md`

### TKT-C02-01 - Implement domain entities and field validators
- Primary SRS: `SRS-FR-001..SRS-FR-004`, `SRS-FR-010`, `SRS-FR-017`, `SRS-NFR-004`
- Requirement consideration: **Global Requirement Consideration** above
- Scope: Define typed entities and validation rules from SRS Section 3.
- Relevant files:
  - `architecture/details/core/02-domain-data-model-and-storage.md`
  - `requirements/SRS_DRAFT.md`
  - `src/simulator/domain/models/simulation_entities.py` (new)
  - `src/simulator/domain/services/model_validation.py` (new)
  - `tests/unit/domain/test_entity_validation.py` (new)
- Done when:
  - All SRS schema constraints are validated with unit tests.
- **Status:** Complete
- **Completed:** `simulation_entities.py`, `model_validation.py`, `tests/unit/domain/test_entity_validation.py`.

### TKT-C02-02 - Implement repository ports and JSON workspace storage adapter
- Primary SRS: `SRS-FR-001..SRS-FR-004`, `SRS-FR-009`, `SRS-FR-021`
- Requirement consideration: **Global Requirement Consideration** above
- Scope: Add repository interfaces plus file-backed implementation with reference integrity checks.
- Relevant files:
  - `architecture/details/core/02-domain-data-model-and-storage.md`
  - `src/simulator/domain/ports/repository_ports.py` (new)
  - `src/simulator/config/workspace_store.py` (new)
  - `src/simulator/config/repository_impl.py` (new)
  - `tests/unit/config/test_workspace_store.py` (new)
  - `tests/unit/config/test_reference_integrity.py` (new)
- Done when:
  - CRUD works for all persisted entities with referential integrity enforcement.
- **Status:** Complete
- **Completed:** `repository_ports.py`, `workspace_store.py`, `repository_impl.py`, unit tests for workspace and reference integrity.

---

## C) Tickets from `core/03-sequence-execution-engine.md`

### TKT-C03-01 - Implement deterministic sequence step runner
- Primary SRS: `SRS-FR-005`, `SRS-FR-006`, `SRS-FR-007`
- Requirement consideration: **Global Requirement Consideration** above
- Scope: Implement ordered step execution loop and step lifecycle transitions.
- Relevant files:
  - `architecture/details/core/03-sequence-execution-engine.md`
  - `src/simulator/workflows/sequence_runner.py` (new)
  - `src/simulator/workflows/step_executor.py` (new)
  - `src/simulator/domain/models/step_result.py` (new)
  - `tests/unit/workflows/test_sequence_runner_order.py` (new)
- Done when:
  - Steps execute strictly by `order_index` with lifecycle state output per step.
- **Status:** Complete
- **Completed:** `sequence_runner.py`, `step_executor.py`, `step_result.py`, `tests/unit/workflows/test_sequence_runner_order.py`.

### TKT-C03-02 - Implement retry and failure policy handling
- Primary SRS: `SRS-FR-005`, `SRS-FR-008`, `SRS-E-RUN-001`
- Requirement consideration: **Global Requirement Consideration** above
- Scope: Add retry policy precedence and final run status logic.
- Relevant files:
  - `architecture/details/core/03-sequence-execution-engine.md`
  - `src/simulator/workflows/sequence_runner.py`
  - `src/simulator/domain/services/run_summary_builder.py` (new)
  - `tests/integration/test_failure_policy_stop_on_fail.py` (new)
  - `tests/integration/test_failure_policy_continue_on_fail.py` (new)
- Done when:
  - `PASS` / `FAIL` / `COMPLETE_WITH_FAILURES` statuses match policy and tests.
- **Status:** Complete
- **Completed:** `run_summary_builder.py`, integration tests for stop/continue failure policy.

---

## D) Tickets from `core/04-task-runtime-and-periodic-scheduler.md`

### TKT-C04-01 - Implement periodic scheduler supervisor
- Primary SRS: `SRS-FR-017`, `SRS-FR-018`, `SRS-NFR-006`
- Requirement consideration: **Global Requirement Consideration** above
- Scope: Add per-run scheduler lifecycle and interval-driven task execution.
- Relevant files:
  - `architecture/details/core/04-task-runtime-and-periodic-scheduler.md`
  - `src/simulator/domain/services/periodic_scheduler.py` (new)
  - `src/simulator/domain/models/periodic_runtime.py` (new)
  - `src/simulator/workflows/periodic_runtime_controller.py` (new)
  - `tests/unit/domain/test_periodic_scheduler_loop.py` (new)
- Done when:
  - Enabled periodic tasks run continuously during active run context.
- **Status:** Complete
- **Completed:** `periodic_scheduler.py`, `periodic_runtime.py`, `periodic_runtime_controller.py`, unit test.

### TKT-C04-02 - Implement overlap policies and runtime ON/OFF API
- Primary SRS: `SRS-FR-018`, `SRS-FR-019`, `SRS-E-RUN-002`, `SRS-E-RUN-003`
- Requirement consideration: **Global Requirement Consideration** above
- Scope: Add `skip`/`queue`/`parallel` behavior and toggle API.
- Relevant files:
  - `architecture/details/core/04-task-runtime-and-periodic-scheduler.md`
  - `src/simulator/domain/services/periodic_scheduler.py`
  - `src/simulator/domain/services/periodic_toggle_service.py` (new)
  - `tests/integration/test_periodic_overlap_policies.py` (new)
  - `tests/integration/test_periodic_toggle_runtime.py` (new)
- Done when:
  - Toggle state applies immediately and overlap behavior matches policy definitions.
- **Status:** Complete
- **Completed:** `periodic_toggle_service.py`, integration tests for overlap and toggle.

---

## E) Tickets from `core/05-transport-adapter-design.md`

### TKT-C05-01 - Implement transport endpoint/config validation
- Primary SRS: `SRS-FR-016`, `SRS-E-VAL-005`, `SRS-E-TRN-001`
- Requirement consideration: **Global Requirement Consideration** above
- Scope: Implement endpoint parser, protocol/mode validation, timeout range checks.
- Relevant files:
  - `architecture/details/core/05-transport-adapter-design.md`
  - `src/simulator/adapters/transport/common/endpoint_parser.py` (new)
  - `src/simulator/adapters/transport/common/transport_validation.py` (new)
  - `src/simulator/domain/ports/transport_port.py` (new)
  - `tests/unit/adapters/transport/test_endpoint_parser.py` (new)
- Done when:
  - Invalid transport configs fail with deterministic error codes.
- **Status:** Complete
- **Completed:** `endpoint_parser.py`, `transport_validation.py`, `tests/unit/adapters/transport/test_endpoint_parser.py`; TransportPort exists.

### TKT-C05-02 - Implement TCP/UDP adapters for client/server flows
- Primary SRS: `SRS-FR-006`, `SRS-FR-016`, `SRS-E-TRN-002..004`
- Requirement consideration: **Global Requirement Consideration** above
- Scope: Add adapter implementations for TCP and UDP send/receive behavior.
- Relevant files:
  - `architecture/details/core/05-transport-adapter-design.md`
  - `src/simulator/adapters/transport/tcp/transport_tcp_adapter.py` (new)
  - `src/simulator/adapters/transport/udp/transport_udp_adapter.py` (new)
  - `src/simulator/adapters/transport/transport_gateway.py` (new)
  - `tests/integration/test_transport_tcp_udp_modes.py` (new)
- Done when:
  - Sequence runner can send/receive through both protocols with mapped errors.
- **Status:** Complete
- **Completed:** `transport_gateway.py`; TCP/UDP via existing `tcp/adapter.py`, `udp/adapter.py`, `composite_transport.py`; integration test added.

---

## F) Tickets from `core/06-verification-engine-design.md`

### TKT-C06-01 - Implement verification rules (exact/subset/absent + count)
- Primary SRS: `SRS-FR-007`, `SRS-FR-008`, `SRS-FR-017`
- Requirement consideration: **Global Requirement Consideration** above
- Scope: Implement rule evaluation order and deterministic verdict generation.
- Relevant files:
  - `architecture/details/core/06-verification-engine-design.md`
  - `src/simulator/domain/services/verification_engine.py` (new)
  - `src/simulator/domain/models/verification_models.py` (new)
  - `tests/unit/domain/test_verification_rules.py` (new)
- Done when:
  - Rule combinations produce correct PASS/FAIL outputs with count assertions.
- **Status:** Complete
- **Completed:** `verification_engine.py`, `verification_models.py`, `tests/unit/domain/test_verification_rules.py`.

### TKT-C06-02 - Implement verification evidence payload and error mapping
- Primary SRS: `SRS-E-VER-001..003`, `SRS-FR-015`
- Requirement consideration: **Global Requirement Consideration** above
- Scope: Build structured evidence and map failure reasons to concrete codes.
- Relevant files:
  - `architecture/details/core/06-verification-engine-design.md`
  - `src/simulator/domain/services/verification_engine.py`
  - `src/simulator/domain/models/verification_result.py` (new)
  - `tests/unit/domain/test_verification_error_mapping.py` (new)
  - `tests/integration/test_verification_failures.py` (new)
- Done when:
  - Failed verification includes required summary fields and exact code mapping.
- **Status:** Complete
- **Completed:** `verification_result.py` (evidence/code), `test_verification_error_mapping.py`, `test_verification_failures.py`.

---

## G) Tickets from `core/07-stateless-boundary-and-run-context.md`

### TKT-C07-01 - Implement RunStateFactory and run context lifecycle
- Primary SRS: `SRS-FR-020`, `SRS-NFR-003`
- Requirement consideration: **Global Requirement Consideration** above
- Scope: Build isolated run context creation and lifecycle APIs.
- Relevant files:
  - `architecture/details/core/07-stateless-boundary-and-run-context.md`
  - `src/simulator/domain/services/run_state_factory.py` (new)
  - `src/simulator/domain/models/run_context.py` (new)
  - `src/simulator/workflows/run_lifecycle.py` (new)
  - `tests/unit/domain/test_run_state_factory.py` (new)
- Done when:
  - Every run gets fresh mutable state with unique run identifiers.
- **Status:** Complete
- **Completed:** `run_state_factory.py`, `run_context.py`, `run_lifecycle.py`, `tests/unit/domain/test_run_state_factory.py`.

### TKT-C07-02 - Enforce teardown and no-state-leakage guarantees
- Primary SRS: `SRS-FR-020`, `SRS-TEST-015`
- Requirement consideration: **Global Requirement Consideration** above
- Scope: Ensure cleanup of scheduler/workers and no mutable carry-over.
- Relevant files:
  - `architecture/details/core/07-stateless-boundary-and-run-context.md`
  - `src/simulator/workflows/run_lifecycle.py`
  - `tests/integration/test_run_state_isolation.py` (new)
  - `tests/integration/test_scheduler_teardown_on_run_end.py` (new)
- Done when:
  - Isolation and teardown tests pass for sequential runs.
- **Status:** Complete
- **Completed:** `run_lifecycle.py` teardown; `test_run_state_isolation.py`, `test_scheduler_teardown_on_run_end.py`.

---

## H) Tickets from `supporting/01-ui-design-gui-tui.md`

### TKT-S01-01 - GUI CRUD screens for core entities
- Primary SRS: `SRS-UI-001`, `SRS-FR-001..SRS-FR-004`
- Requirement consideration: **Global Requirement Consideration** above
- Scope: Build GUI CRUD for applications/targets/contracts/tasks/transports/messages/expectations/sequences.
- **Mandatory GUI note:** Use `py-gui` (`/workspace/py-gui`) with `tk-mvc` patterns.
- Relevant files:
  - `architecture/details/supporting/01-ui-design-gui-tui.md`
  - `src/simulator/adapters/ui/gui/controllers/crud_controller.py` (new)
  - `src/simulator/adapters/ui/gui/views/crud_views.py` (new)
  - `src/simulator/adapters/ui/gui/presenters/crud_presenter.py` (new)
  - `tests/e2e/test_gui_crud_smoke.py` (new)
- Done when:
  - GUI can create/edit/delete each entity and display validation feedback.
- **Status:** Complete
- **Completed:** `crud_controller.py`, `crud_views.py`, `crud_presenter.py`, `tests/e2e/test_gui_crud_smoke.py`.

### TKT-S01-02 - GUI run timeline and periodic task ON/OFF controls
- Primary SRS: `SRS-UI-002`, `SRS-UI-006`, `SRS-UI-008`, `SRS-FR-019`
- Requirement consideration: **Global Requirement Consideration** above
- Scope: Add live timeline and periodic toggle controls/status panel.
- **Mandatory GUI note:** Use `py-gui` (`/workspace/py-gui`) with `tk-mvc` patterns.
- Relevant files:
  - `architecture/details/supporting/01-ui-design-gui-tui.md`
  - `src/simulator/adapters/ui/gui/controllers/run_monitor_controller.py` (new)
  - `src/simulator/adapters/ui/gui/views/run_timeline_view.py` (new)
  - `src/simulator/adapters/ui/gui/views/periodic_toggle_view.py` (new)
  - `tests/e2e/test_gui_periodic_toggle.py` (new)
- Done when:
  - User can toggle periodic task ON/OFF and see live execution timeline updates.
- **Status:** Complete
- **Completed:** `run_monitor_controller.py`, `run_timeline_view.py`, `periodic_toggle_view.py`, e2e test.

### TKT-S01-03 - TUI CRUD flows with parity to GUI capabilities
- Primary SRS: `SRS-UI-003`, `SRS-UI-004`, `SRS-FR-013`
- Requirement consideration: **Global Requirement Consideration** above
- Scope: Implement TUI entity CRUD with parity for core operations.
- Relevant files:
  - `architecture/details/supporting/01-ui-design-gui-tui.md`
  - `src/simulator/adapters/ui/tui/screens/config_screen.py` (new)
  - `src/simulator/adapters/ui/tui/commands/crud_commands.py` (new)
  - `src/simulator/adapters/ui/tui/presenters/config_presenter.py` (new)
  - `tests/e2e/test_tui_crud_smoke.py` (new)
- Done when:
  - TUI supports equivalent CRUD flows and returns equivalent outcomes.
- **Status:** Complete
- **Completed:** `config_screen.py`, `crud_commands.py`, `config_presenter.py`, e2e test.

### TKT-S01-04 - TUI run monitor and periodic toggle command
- Primary SRS: `SRS-UI-007`, `SRS-UI-008`, `SRS-FR-019`
- Requirement consideration: **Global Requirement Consideration** above
- Scope: Add run monitor screen and periodic ON/OFF command/action.
- Relevant files:
  - `architecture/details/supporting/01-ui-design-gui-tui.md`
  - `src/simulator/adapters/ui/tui/screens/run_screen.py` (new)
  - `src/simulator/adapters/ui/tui/commands/periodic_toggle_command.py` (new)
  - `src/simulator/adapters/ui/tui/presenters/run_presenter.py` (new)
  - `tests/e2e/test_tui_periodic_toggle.py` (new)
- Done when:
  - TUI can toggle periodic tasks and show current runtime status fields.
- **Status:** Complete
- **Completed:** `run_screen.py`, `periodic_toggle_command.py`, `run_presenter.py`, e2e test.

---

## I) Tickets from `supporting/02-validation-and-error-model.md`

### TKT-S02-01 - Implement centralized validation pipeline
- Primary SRS: `SRS-E-VAL-001..006`, `SRS-FR-001..SRS-FR-004`
- Requirement consideration: **Global Requirement Consideration** above
- Scope: Build CRUD-time, pre-run, and runtime validators.
- Relevant files:
  - `architecture/details/supporting/02-validation-and-error-model.md`
  - `src/simulator/domain/services/validation_service.py` (new)
  - `src/simulator/workflows/pre_run_validation.py` (new)
  - `src/simulator/domain/models/validation_result.py` (new)
  - `tests/unit/domain/test_validation_service.py` (new)
- Done when:
  - Validation phase outputs are deterministic and error-code mapped.
- **Status:** Complete
- **Completed:** `validation_service.py`, `pre_run_validation.py`, `validation_result.py`, unit test.

### TKT-S02-02 - Implement standardized error envelope and catalog module
- Primary SRS: Section 11, `SRS-E-*`, `SRS-FR-015`
- Requirement consideration: **Global Requirement Consideration** above
- Scope: Add error code catalog and envelope builder used by all layers.
- Relevant files:
  - `architecture/details/supporting/02-validation-and-error-model.md`
  - `src/simulator/domain/models/error_envelope.py` (new)
  - `src/simulator/domain/services/error_catalog.py` (new)
  - `src/simulator/domain/services/error_factory.py` (new)
  - `tests/unit/domain/test_error_envelope_contract.py` (new)
- Done when:
  - All emitted errors conform to required envelope fields and codes.
- **Status:** Complete
- **Completed:** `error_envelope.py`, `error_catalog.py`, `error_factory.py`, `test_error_envelope_contract.py`.

---

## J) Tickets from `supporting/03-observability-and-nfr-design.md`

### TKT-S03-01 - Implement structured logging and redaction
- Primary SRS: `SRS-FR-015`, `SRS-NFR-002`
- Requirement consideration: **Global Requirement Consideration** above
- Scope: Add structured logger and redaction utility for sensitive fields.
- Relevant files:
  - `architecture/details/supporting/03-observability-and-nfr-design.md`
  - `src/simulator/logging/structured_logger.py` (new)
  - `src/simulator/logging/redaction.py` (new)
  - `src/simulator/logging/log_event_schema.py` (new)
  - `tests/unit/logging/test_redaction.py` (new)
- Done when:
  - Lifecycle events are logged with redaction and correlation metadata.
- **Status:** Complete
- **Completed:** `structured_logger.py`, `redaction.py`, `log_event_schema.py`, `tests/unit/logging/test_redaction.py`.

### TKT-S03-02 - Implement metrics collector and baseline NFR benchmark script
- Primary SRS: `SRS-NFR-006`, `SRS-NFR-007`, `SRS-NFR-008`
- Requirement consideration: **Global Requirement Consideration** above
- Scope: Add counters/timers/gauges plus script for baseline capacity/latency checks.
- Relevant files:
  - `architecture/details/supporting/03-observability-and-nfr-design.md`
  - `src/simulator/domain/services/metrics_collector.py` (new)
  - `scripts/nfr_benchmark.py` (new)
  - `tests/perf/test_capacity_baseline.py` (new)
  - `tests/perf/test_latency_baseline.py` (new)
- Done when:
  - Metrics are emitted and benchmark script reports pass/fail vs SRS thresholds.
- **Status:** Complete
- **Completed:** `metrics_collector.py`, `scripts/nfr_benchmark.py`, perf tests for capacity/latency baseline.

---

## K) Tickets from `supporting/04-test-traceability-and-quality-gates.md`

### TKT-S04-01 - Implement FR-to-test traceability checks
- Primary SRS: `SRS-FR-021`, Section 13.1, Section 14
- Requirement consideration: **Global Requirement Consideration** above
- Scope: Enforce mapping between functional requirements and tests.
- Relevant files:
  - `architecture/details/supporting/04-test-traceability-and-quality-gates.md`
  - `requirements/SRS_DRAFT.md`
  - `tests/traceability/test_fr_to_test_mapping.py` (new)
  - `scripts/ci_test_runner.py`
- Done when:
  - CI fails if mapped FR coverage is missing or stale.
- **Status:** Complete
- **Completed:** `tests/traceability/test_fr_to_test_mapping.py`, `scripts/ci_test_runner.py`.

### TKT-S04-02 - Implement critical regression suites in CI
- Primary SRS: `SRS-NFR-004`, `SRS-NFR-005`, `SRS-TEST-002..018`
- Requirement consideration: **Global Requirement Consideration** above
- Scope: Add required regression suites and wire into CI scripts.
- Relevant files:
  - `architecture/details/supporting/04-test-traceability-and-quality-gates.md`
  - `scripts/ci_test_runner.py`
  - `scripts/gui_tui_smoke_check.py`
  - `tests/integration/test_periodic_parallel_flow.py` (new)
  - `tests/integration/test_stateless_boundary.py` (new)
- Done when:
  - CI executes required regression suites and blocks on failures.
- **Status:** Complete
- **Completed:** `ci_test_runner.py`, `gui_tui_smoke_check.py`, `test_periodic_parallel_flow.py`, `test_stateless_boundary.py`.

---

## Suggested Implementation Order

1. Core foundation: `TKT-C01-*`, `TKT-C02-*`
2. Execution and verification: `TKT-C03-*`, `TKT-C06-*`
3. Transport and scheduler: `TKT-C05-*`, `TKT-C04-*`
4. Stateless and cleanup: `TKT-C07-*`
5. Validation/errors/observability: `TKT-S02-*`, `TKT-S03-*`
6. UI parity and controls: `TKT-S01-*`
7. Traceability and CI hardening: `TKT-S04-*`
