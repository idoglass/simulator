# Software Requirements Specification (SRS) - Draft v0.2

## Document Metadata

- Product: Simulator
- Document: `requirements/SRS_DRAFT.md`
- Version: 0.2
- Status: Draft
- Date: 2026-02-20

## 1. Purpose

Define the software requirements for a simulator that:

1. Sends messages to a target.
2. Verifies received responses against user-defined expectations.
3. Supports multi-step execution flows and multiple simulated applications.

This revision expands the initial draft with concrete functional boundaries, constraints, acceptance criteria, and traceability to baseline GR IDs.

## 2. Scope

The simulator SHALL provide:

1. Definition of target, message, and expected response.
2. Definition and execution of ordered sequences of message/verification steps.
3. Management of any number of simulated applications.
4. Per-application management of contracts, tasks, and transport definitions.
5. GUI and TUI interfaces backed by one shared simulation engine.
6. Real-time action visibility during execution.
7. CRUD support for all primary entities.

## 3. In-Scope Entities and Minimum Data Model

| Entity | Required Fields (minimum) | Notes |
| --- | --- | --- |
| SimulatedApplication | `app_id`, `app_name` | `app_name` must be unique in workspace. |
| TargetDefinition | `target_id`, `target_name`, `application_ref`, `transport_ref` | A target belongs to one application context. |
| ContractDefinition | `contract_id`, `application_ref`, `source_type`, `source_path`, `version` | `source_type` in `{repo_h, user_h}`. |
| TaskDefinition | `task_id`, `application_ref`, `task_name`, `registration_type`, `task_ref` | `registration_type` in `{built_in, runtime_loaded}`. |
| TransportDefinition | `transport_id`, `application_ref`, `protocol`, `mode`, `local_endpoint`, `remote_endpoint` | `protocol` in `{tcp, udp}`; `mode` in `{client, server}`. |
| MessageDefinition | `message_id`, `target_ref`, `contract_ref`, `message_type`, `payload_binding` | `payload_binding` must map to `.h`/`ctypes` model. |
| ExpectedResponse | `expectation_id`, `message_ref`, `match_rule`, `assertion` | MVP assertion must include count-based support. |
| SequenceDefinition | `sequence_id`, `application_ref`, `sequence_name`, `steps`, `failure_policy` | `steps` is ordered list of step references. |
| SequenceStep | `step_id`, `sequence_ref`, `order_index`, `message_ref`, `expectation_ref` | `order_index` starts at 1 and must be unique per sequence. |

## 4. Functional Requirements

| ID | Requirement | Acceptance Criteria | Mapped GR IDs |
| --- | --- | --- | --- |
| SRS-FR-001 | The system SHALL allow create/read/update/delete for SimulatedApplication. | CRUD operations succeed for valid input; delete is blocked if dependent entities exist unless explicitly forced by policy. | GR-008, GR-025 |
| SRS-FR-002 | The system SHALL allow CRUD for TargetDefinition, MessageDefinition, and ExpectedResponse. | User can persist definitions and retrieve exact saved values. | GR-019, GR-020 |
| SRS-FR-003 | The system SHALL allow CRUD for ContractDefinition, TaskDefinition, and TransportDefinition. | Each entity type supports create/read/update/delete with validation feedback. | GR-009, GR-022, GR-023, GR-031 |
| SRS-FR-004 | The system SHALL allow CRUD for SequenceDefinition and SequenceStep. | Ordered steps are persisted, reordered, and validated before run. | GR-019, GR-020 |
| SRS-FR-005 | The system SHALL execute a selected sequence in deterministic step order. | Execution order equals ascending `order_index`; run result includes per-step status. | GR-019, GR-020 |
| SRS-FR-006 | The system SHALL send each step message to the configured target endpoint. | For each executed step, send attempt is logged with correlation/run identifiers. | GR-020, GR-031, GR-059 |
| SRS-FR-007 | The system SHALL verify each observed response against the associated expected response. | Each step reports PASS/FAIL with reason when response does not satisfy rule. | GR-030 |
| SRS-FR-008 | The system SHALL support count-based verification assertions in MVP. | User can assert expected response count and obtain pass/fail result. | GR-030 |
| SRS-FR-009 | The system SHALL support multiple simulated applications in one workspace. | Definitions for one application do not overwrite another application's definitions. | GR-008 |
| SRS-FR-010 | The system SHALL enforce that simulation payload definitions come from `.h`/`ctypes` metadata. | Invalid or unknown type bindings are rejected before execution. | GR-009, GR-022 |
| SRS-FR-011 | The system SHALL execute simulation behavior only through registered tasks. | Unregistered task references fail validation and run is blocked. | GR-023 |
| SRS-FR-012 | The system SHALL support runtime task loading/registration before execution. | Newly loaded task can be referenced by a sequence without app restart. | GR-028 |
| SRS-FR-013 | The GUI and TUI SHALL expose equivalent core capabilities. | Equivalent input definitions produce equivalent execution outcomes on both interfaces. | GR-012, GR-025, GR-026 |
| SRS-FR-014 | The GUI SHALL show execution actions as they happen. | Action timeline updates during run and includes at minimum: run start, step send, step verify, run end. | GR-059 |
| SRS-FR-015 | The system SHALL emit structured lifecycle logs with sensitive data redaction. | Required lifecycle events are logged; sensitive fields are redacted per policy. | GR-059 |
| SRS-FR-016 | The simulator SHALL support TCP/UDP transport in client/server modes. | Valid configurations execute on supported protocol/mode combinations. | GR-031 |

## 5. Sequence Execution Semantics

1. A sequence is valid only if all referenced entities exist and pass validation.
2. Steps execute strictly in ascending `order_index`.
3. Each step transitions through statuses: `PENDING -> SENT -> VERIFIED` or `FAILED`.
4. Run status is:
   - `PASS` when all steps pass verification.
   - `FAIL` when any step fails and failure policy is `stop_on_fail`.
   - `COMPLETE_WITH_FAILURES` when failure policy is `continue_on_fail` and at least one step fails.
5. Default `failure_policy` is `stop_on_fail`.
6. Retry and timeout policy is in scope but exact numeric defaults are TBD in v0.3.

## 6. Response Verification Rules (MVP)

1. Each step MUST define one `ExpectedResponse`.
2. Verification MUST support:
   - response presence/absence checks
   - count-based assertions (required MVP)
3. Match-rule operators for MVP:
   - `exact` (full expected payload equality)
   - `subset` (expected fields must exist and match)
4. A failed verification MUST report:
   - step identifier
   - expected rule summary
   - observed response summary (or timeout/no response)
   - failure reason code

## 7. Transport Requirements

1. Supported protocols: TCP and UDP.
2. Supported modes per protocol: client and server.
3. Each target/sequence execution must bind to one transport definition.
4. Invalid endpoint configuration SHALL fail pre-run validation.
5. Transport execution events SHALL be visible in GUI timeline and logs.

## 8. Task and Contract Constraints

1. Message payload/type binding SHALL come only from `.h`/`ctypes` contract sources.
2. Task execution SHALL be restricted to registered tasks.
3. Runtime-loaded tasks SHALL be validated before use in sequence execution.
4. Contract/task validation failures SHALL prevent run start.

## 9. UI Requirements (GUI and TUI)

| ID | Surface | Requirement | Acceptance Criteria |
| --- | --- | --- | --- |
| SRS-UI-001 | GUI | GUI shall support CRUD for all in-scope entities. | Each entity has create/edit/delete and detail view flow. |
| SRS-UI-002 | GUI | GUI shall show run actions in near real time. | User sees run state transitions and per-step outcomes during execution. |
| SRS-UI-003 | TUI | TUI shall expose equivalent core configuration and run capabilities. | User can define/run/verify equivalent flows via TUI commands/screens. |
| SRS-UI-004 | Both | GUI and TUI shall use one shared engine. | Equivalent definitions yield equivalent pass/fail outcomes. |
| SRS-UI-005 | Both | User help documentation shall exist in GUI Help and TUI help/man. | Help includes target/message/sequence/verification/task/transport usage. |

## 10. Statelessness Boundary

1. The application layer SHALL NOT keep mutable run state between independent runs.
2. Persisted configuration artifacts (saved definitions) are allowed.
3. Runtime execution state (active step status, in-flight transport correlation, temporary counters) is per-run only.
4. Starting a new run SHALL initialize a new run context and identifiers.

## 11. Error Handling and Diagnostics

1. Validation errors SHALL be reported before run start when possible.
2. Runtime errors SHALL include actionable reason and affected entity/step.
3. Minimum error categories:
   - `VALIDATION_ERROR`
   - `TRANSPORT_ERROR`
   - `VERIFICATION_ERROR`
   - `TASK_REGISTRATION_ERROR`
   - `INTERNAL_ERROR`
4. Detailed error code catalog is TBD for v0.3.

## 12. Non-Functional Requirements

| ID | Requirement | Target/Rule | Mapped GR IDs |
| --- | --- | --- | --- |
| SRS-NFR-001 | Portability | MVP support on Windows and Linux. | GR-011 |
| SRS-NFR-002 | Logging and observability | Emit verbose lifecycle logs with runtime-configurable level and redaction. | GR-059 |
| SRS-NFR-003 | Architecture consistency | GUI/TUI use shared engine and MVC boundaries. | GR-026, GR-058 |
| SRS-NFR-004 | Testability | Unit tests for major components and simple e2e for critical flows. | GR-039 |
| SRS-NFR-005 | CI quality gates | Lint and tests required in CI quality pipeline. | GR-040 |

## 13. Validation and Test Scenarios (High Level)

| Test ID | Scenario | Expected Result |
| --- | --- | --- |
| SRS-TEST-001 | Create app/target/message/expected-response and save. | Definitions are persisted and reload correctly. |
| SRS-TEST-002 | Run a 3-step valid sequence. | Run returns PASS and all steps verified. |
| SRS-TEST-003 | Run sequence with mismatched expected response. | Step fails with VERIFICATION_ERROR details. |
| SRS-TEST-004 | Use unregistered task in sequence. | Pre-run validation fails and run does not start. |
| SRS-TEST-005 | Execute same scenario via GUI and TUI. | Equivalent outcome and verification summary. |
| SRS-TEST-006 | Configure invalid transport endpoint. | Validation fails with TRANSPORT_ERROR. |
| SRS-TEST-007 | Run on Linux and Windows smoke path. | Core sequence execution is successful on both OS targets. |

## 14. Traceability Map to General Requirements

| SRS Requirement IDs | GR IDs |
| --- | --- |
| SRS-FR-001..SRS-FR-004 | GR-019, GR-020, GR-025 |
| SRS-FR-005..SRS-FR-009 | GR-008, GR-019, GR-020, GR-030 |
| SRS-FR-010..SRS-FR-012 | GR-009, GR-022, GR-023, GR-028 |
| SRS-FR-013..SRS-FR-016 | GR-012, GR-025, GR-026, GR-031, GR-059 |
| SRS-UI-001..SRS-UI-005 | GR-012, GR-025, GR-026, GR-057 |
| SRS-NFR-001..SRS-NFR-005 | GR-011, GR-039, GR-040, GR-058, GR-059 |

## 15. Open Items for Next Revision (v0.3)

1. Finalize numeric timeout/retry defaults.
2. Define complete error code catalog and remediation guidance.
3. Define full field-level schema (types, ranges, defaults) for all entities.
4. Add measurable capacity/performance targets.
5. Add full test matrix and pass thresholds.
