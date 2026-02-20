# Software Requirements Specification (SRS) - Draft v0.3

## Document Metadata

- Product: Simulator
- Document: `requirements/SRS_DRAFT.md`
- Version: 0.3
- Status: Draft
- Date: 2026-02-20

## 1. Purpose

Define the software requirements for a simulator that:

1. Sends messages to a target.
2. Verifies received responses against user-defined expectations.
3. Supports multi-step execution flows and multiple simulated applications.

This revision expands the initial draft with concrete functional boundaries, field-level schemas, error codes, acceptance criteria, and traceability to baseline GR IDs.

## 2. Scope

The simulator SHALL provide:

1. Definition of target, message, and expected response.
2. Definition and execution of ordered sequences of message/verification steps.
3. Management of any number of simulated applications.
4. Per-application management of contracts, tasks, and transport definitions.
5. GUI and TUI interfaces backed by one shared simulation engine.
6. Real-time action visibility during execution.
7. CRUD support for all primary entities.
8. Optional periodic task execution that runs continuously in parallel with other tasks.
9. UI controls to switch periodic tasks on and off at runtime.

## 3. Field-Level Schemas (Types, Defaults, Ranges)

### 3.1 Common Type Rules

- **ID fields:** `string`, regex `^[A-Za-z0-9._-]{1,64}$`
- **Name fields:** `string`, length `1..128`, trimmed, non-empty
- **Timestamp fields:** UTC ISO-8601 string (example: `2026-02-20T15:04:05Z`)
- **Endpoint format:** `host:port` where `port` is integer `1..65535`
- **Boolean defaults:** explicit (`true`/`false`), never null

### 3.2 SimulatedApplication

| Field | Type | Required | Default | Allowed / Range | Notes |
| --- | --- | --- | --- | --- | --- |
| app_id | string | Yes | N/A | ID regex | Stable unique identifier. |
| app_name | string | Yes | N/A | length 1..128 | Unique across workspace. |
| description | string | No | `""` | length 0..512 | User-readable notes. |
| enabled | boolean | No | `true` | `true`/`false` | Disabled apps cannot run sequences. |

### 3.3 TargetDefinition

| Field | Type | Required | Default | Allowed / Range | Notes |
| --- | --- | --- | --- | --- | --- |
| target_id | string | Yes | N/A | ID regex | Unique target identifier. |
| target_name | string | Yes | N/A | length 1..128 | Display name. |
| application_ref | string | Yes | N/A | ID regex | Must reference existing app. |
| transport_ref | string | Yes | N/A | ID regex | Must reference existing transport. |
| timeout_ms | integer | No | `5000` | `100..120000` | Per-target response timeout. |
| retry_count | integer | No | `1` | `0..10` | Send/receive retry attempts. |

### 3.4 ContractDefinition

| Field | Type | Required | Default | Allowed / Range | Notes |
| --- | --- | --- | --- | --- | --- |
| contract_id | string | Yes | N/A | ID regex | Unique contract identifier. |
| application_ref | string | Yes | N/A | ID regex | Owner app. |
| source_type | enum | Yes | N/A | `repo_h`, `user_h` | `.h` source origin. |
| source_path | string | Yes | N/A | length 1..512 | Path to `.h` source. |
| version | string | No | `0.1.0` | semver-like `X.Y.Z` | Contract revision label. |
| checksum_sha256 | string | No | `""` | 64 hex chars or empty | Optional integrity marker. |

### 3.5 TaskDefinition

| Field | Type | Required | Default | Allowed / Range | Notes |
| --- | --- | --- | --- | --- | --- |
| task_id | string | Yes | N/A | ID regex | Unique task identifier. |
| application_ref | string | Yes | N/A | ID regex | Owner app. |
| task_name | string | Yes | N/A | length 1..128 | Display name. |
| registration_type | enum | Yes | N/A | `built_in`, `runtime_loaded` | Registration source. |
| task_ref | string | Yes | N/A | length 1..256 | Registered task key/path. |
| execution_mode | enum | No | `oneshot` | `oneshot`, `periodic` | Runtime execution style. |
| periodic_config | object | Conditional | `{}` | see Section 3.5.1 | Required when `execution_mode=periodic`. |

#### 3.5.1 periodic_config

| Field | Type | Required | Default | Allowed / Range | Notes |
| --- | --- | --- | --- | --- | --- |
| enabled | boolean | No | `false` | `true`/`false` | UI can toggle at runtime. |
| interval_ms | integer | Yes (periodic) | `1000` | `100..86400000` | Scheduler period (0.1s to 24h). |
| jitter_pct | integer | No | `0` | `0..30` | Optional random spread to avoid thundering herd. |
| overlap_policy | enum | No | `skip` | `skip`, `queue`, `parallel` | Behavior when next interval arrives while running. |
| max_parallel_runs | integer | Conditional | `1` | `1..32` | Used only when `overlap_policy=parallel`. |
| auto_start | boolean | No | `false` | `true`/`false` | Start automatically at run start. |

### 3.6 TransportDefinition

| Field | Type | Required | Default | Allowed / Range | Notes |
| --- | --- | --- | --- | --- | --- |
| transport_id | string | Yes | N/A | ID regex | Unique transport identifier. |
| application_ref | string | Yes | N/A | ID regex | Owner app. |
| protocol | enum | No | `tcp` | `tcp`, `udp` | Supported transport protocol. |
| mode | enum | No | `client` | `client`, `server` | Runtime mode. |
| local_endpoint | string | Conditional | `""` | endpoint format or empty | Required for server mode. |
| remote_endpoint | string | Conditional | `""` | endpoint format or empty | Required for client mode. |
| connect_timeout_ms | integer | No | `3000` | `100..60000` | Connection setup timeout. |
| read_timeout_ms | integer | No | `5000` | `100..120000` | Read timeout. |
| write_timeout_ms | integer | No | `5000` | `100..120000` | Write timeout. |
| max_packet_bytes | integer | No | `65535` | `1..1048576` | Transport packet safety limit. |

### 3.7 MessageDefinition

| Field | Type | Required | Default | Allowed / Range | Notes |
| --- | --- | --- | --- | --- | --- |
| message_id | string | Yes | N/A | ID regex | Unique message identifier. |
| target_ref | string | Yes | N/A | ID regex | Must reference existing target. |
| contract_ref | string | Yes | N/A | ID regex | Must reference existing contract. |
| message_type | string | Yes | N/A | length 1..128 | Contract-defined message type. |
| payload_binding | string | Yes | N/A | length 1..256 | `.h`/`ctypes` structure binding key. |
| payload_values | object | No | `{}` | JSON object | Runtime payload values. |
| send_timeout_ms | integer | No | `5000` | `100..120000` | Send timeout. |
| expect_response | boolean | No | `true` | `true`/`false` | Whether verification is expected. |

### 3.8 ExpectedResponse

| Field | Type | Required | Default | Allowed / Range | Notes |
| --- | --- | --- | --- | --- | --- |
| expectation_id | string | Yes | N/A | ID regex | Unique expectation identifier. |
| message_ref | string | Yes | N/A | ID regex | Must reference message. |
| match_rule | enum | No | `exact` | `exact`, `subset`, `absent` | Payload match behavior. |
| assertion_count | integer | No | `1` | `0..100000` | Required count assertion (MVP). |
| assertion_window_ms | integer | No | `5000` | `100..300000` | Verification collection window. |
| required_fields | array[string] | No | `[]` | max 256 entries | Required when `match_rule=subset`. |
| allow_extra_fields | boolean | No | `true` | `true`/`false` | Extra fields allowed in observed response. |

### 3.9 SequenceDefinition

| Field | Type | Required | Default | Allowed / Range | Notes |
| --- | --- | --- | --- | --- | --- |
| sequence_id | string | Yes | N/A | ID regex | Unique sequence identifier. |
| application_ref | string | Yes | N/A | ID regex | Owner app. |
| sequence_name | string | Yes | N/A | length 1..128 | Display name. |
| failure_policy | enum | No | `stop_on_fail` | `stop_on_fail`, `continue_on_fail` | Failure handling mode. |
| step_timeout_ms | integer | No | `5000` | `100..120000` | Default timeout for step execution. |
| max_duration_ms | integer | No | `300000` | `1000..3600000` | Hard run duration ceiling. |
| enabled | boolean | No | `true` | `true`/`false` | Disabled sequences cannot run. |

### 3.10 SequenceStep

| Field | Type | Required | Default | Allowed / Range | Notes |
| --- | --- | --- | --- | --- | --- |
| step_id | string | Yes | N/A | ID regex | Unique step identifier. |
| sequence_ref | string | Yes | N/A | ID regex | Must reference sequence. |
| order_index | integer | Yes | N/A | `1..10000` | Unique within sequence. |
| message_ref | string | Yes | N/A | ID regex | Must reference message. |
| expectation_ref | string | Yes | N/A | ID regex | Must reference expectation. |
| enabled | boolean | No | `true` | `true`/`false` | Disabled steps are skipped. |
| delay_before_ms | integer | No | `0` | `0..600000` | Delay before send. |
| retry_count | integer | No | `0` | `0..10` | Step-level retries. |

### 3.11 PeriodicTaskRuntime

| Field | Type | Required | Default | Allowed / Range | Notes |
| --- | --- | --- | --- | --- | --- |
| runtime_id | string | Yes | N/A | ID regex | Runtime scheduler instance ID. |
| task_ref | string | Yes | N/A | ID regex | Must reference periodic task. |
| enabled | boolean | No | `false` | `true`/`false` | Current runtime enabled state. |
| interval_ms | integer | No | `1000` | `100..86400000` | Active interval in milliseconds. |
| last_run_at | string/null | No | `null` | ISO-8601 UTC or null | Last completed execution timestamp. |
| next_run_at | string/null | No | `null` | ISO-8601 UTC or null | Scheduled next runtime. |
| run_count | integer | No | `0` | `0..2147483647` | Successful + failed iterations count. |
| consecutive_failures | integer | No | `0` | `0..100000` | Last uninterrupted failure streak. |

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
| SRS-FR-017 | The system SHALL allow a task to be configured as periodic and continuously executed. | When periodic mode is enabled, the task executes repeatedly at configured interval until turned off or run context ends. | GR-020, GR-023 |
| SRS-FR-018 | The system SHALL execute enabled periodic tasks in parallel with other task/sequence execution. | Periodic task execution continues while foreground sequence steps run; foreground flow is not blocked by scheduler loop. | GR-020, GR-023, GR-026 |
| SRS-FR-019 | The system SHALL expose runtime on/off controls for periodic task execution. | User can switch periodic task ON/OFF from UI; state change takes effect without app restart. | GR-025, GR-026 |

## 5. Sequence Execution Semantics

1. A sequence is valid only if all referenced entities exist and pass validation.
2. Steps execute strictly in ascending `order_index`.
3. Each step transitions through statuses: `PENDING -> SENT -> VERIFIED` or `FAILED`.
4. Run status is:
   - `PASS` when all steps pass verification.
   - `FAIL` when any step fails and failure policy is `stop_on_fail`.
   - `COMPLETE_WITH_FAILURES` when failure policy is `continue_on_fail` and at least one step fails.
5. Default `failure_policy` is `stop_on_fail`.
6. Default sequence timeout and retry policy:
   - `step_timeout_ms` default is `5000`.
   - `retry_count` default is `0` at step level and `1` at target level.
   - Transport connect/read/write defaults are in Section 3.6.
7. Enabled periodic tasks may run before, during, and after sequence execution within the same run context.
8. Periodic execution is independent of sequence step ordering and runs on scheduler interval.
9. Switching a periodic task OFF stops future iterations; an in-flight iteration is allowed to finish gracefully.
10. Overlap policy behavior for periodic tasks:
    - `skip`: skip triggering a new run if prior run is still in-flight.
    - `queue`: allow one pending trigger; additional triggers are dropped.
    - `parallel`: permit concurrent runs up to `max_parallel_runs`.

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
5. Count-based assertions SHALL be applicable to responses produced by periodic tasks.

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
5. Periodic task configuration SHALL include a positive interval (`interval_ms > 0`).
6. A periodic task MAY be switched on/off during an active run.
7. Invalid periodic configuration SHALL fail validation and SHALL NOT start scheduler execution.

## 9. UI Requirements (GUI and TUI)

| ID | Surface | Requirement | Acceptance Criteria |
| --- | --- | --- | --- |
| SRS-UI-001 | GUI | GUI shall support CRUD for all in-scope entities. | Each entity has create/edit/delete and detail view flow. |
| SRS-UI-002 | GUI | GUI shall show run actions in near real time. | User sees run state transitions and per-step outcomes during execution. |
| SRS-UI-003 | TUI | TUI shall expose equivalent core configuration and run capabilities. | User can define/run/verify equivalent flows via TUI commands/screens. |
| SRS-UI-004 | Both | GUI and TUI shall use one shared engine. | Equivalent definitions yield equivalent pass/fail outcomes. |
| SRS-UI-005 | Both | User help documentation shall exist in GUI Help and TUI help/man. | Help includes target/message/sequence/verification/task/transport usage. |
| SRS-UI-006 | GUI | GUI shall provide an ON/OFF switch for each periodic-capable task. | User can toggle task state and see current enabled/disabled state immediately. |
| SRS-UI-007 | TUI | TUI shall provide command/action to turn periodic tasks ON/OFF. | User can toggle state from TUI and receive immediate state feedback. |
| SRS-UI-008 | Both | UI shall display periodic task runtime status. | UI shows at minimum: enabled state, interval, and last-run timestamp. |

## 10. Statelessness Boundary

1. The application layer SHALL NOT keep mutable run state between independent runs.
2. Persisted configuration artifacts (saved definitions) are allowed.
3. Runtime execution state (active step status, in-flight transport correlation, temporary counters) is per-run only.
4. Starting a new run SHALL initialize a new run context and identifiers.

## 11. Error Handling and Diagnostics

1. Validation errors SHALL be reported before run start when possible.
2. Runtime errors SHALL include actionable reason and affected entity/step.
3. Every emitted error SHALL include:
   - `error_code`
   - `category`
   - `message`
   - `entity_type`
   - `entity_id`
   - `run_id`
   - `step_id` (if applicable)
   - `timestamp_utc`
   - `recoverable` (`true`/`false`)

### 11.1 Error Code Table (Concrete)

| Error Code | Category | Trigger Condition | System Behavior | Recoverable |
| --- | --- | --- | --- | --- |
| SRS-E-VAL-001 | VALIDATION_ERROR | Required field missing | Reject create/update/run request | Yes |
| SRS-E-VAL-002 | VALIDATION_ERROR | Field out of allowed range/type | Reject request; include field path | Yes |
| SRS-E-VAL-003 | VALIDATION_ERROR | Invalid entity reference (missing `*_ref`) | Reject request; include missing reference | Yes |
| SRS-E-VAL-004 | VALIDATION_ERROR | Duplicate `app_name` in workspace | Reject app create/update | Yes |
| SRS-E-VAL-005 | VALIDATION_ERROR | Invalid endpoint format (`host:port`) | Reject transport save/run | Yes |
| SRS-E-VAL-006 | VALIDATION_ERROR | Invalid periodic config (`interval_ms <= 0`, bad overlap config) | Reject periodic enable/start | Yes |
| SRS-E-TASK-001 | TASK_REGISTRATION_ERROR | Task reference not registered | Block run start | Yes |
| SRS-E-TASK-002 | TASK_REGISTRATION_ERROR | Runtime task load/registration failed | Block dependent run paths | Yes |
| SRS-E-TRN-001 | TRANSPORT_ERROR | Connection open failed | Mark step failed; apply retry policy | Yes |
| SRS-E-TRN-002 | TRANSPORT_ERROR | Send timeout reached | Mark step failed; apply retry policy | Yes |
| SRS-E-TRN-003 | TRANSPORT_ERROR | Receive timeout reached | Mark step failed; continue or abort per policy | Yes |
| SRS-E-TRN-004 | TRANSPORT_ERROR | Connection closed/reset by peer during run | Mark step failed; log peer reset details | Yes |
| SRS-E-VER-001 | VERIFICATION_ERROR | Expected response not observed within window | Step verification failed | Yes |
| SRS-E-VER-002 | VERIFICATION_ERROR | Count assertion mismatch | Step verification failed with expected vs observed counts | Yes |
| SRS-E-VER-003 | VERIFICATION_ERROR | Payload mismatch for `exact`/`subset` rule | Step verification failed with mismatch summary | Yes |
| SRS-E-RUN-001 | RUN_POLICY_ERROR | Sequence aborted by `stop_on_fail` policy | Set run status to `FAIL` and stop next steps | No |
| SRS-E-RUN-002 | RUN_POLICY_ERROR | Periodic trigger skipped due to `overlap_policy=skip` | Emit warning event and continue scheduler | Yes |
| SRS-E-RUN-003 | RUN_POLICY_ERROR | Periodic queue overflow under `overlap_policy=queue` | Drop extra trigger and emit warning | Yes |
| SRS-E-INT-001 | INTERNAL_ERROR | Unexpected unhandled exception | Mark run failed and preserve diagnostic context | No |

## 12. Non-Functional Requirements

| ID | Requirement | Target/Rule | Mapped GR IDs |
| --- | --- | --- | --- |
| SRS-NFR-001 | Portability | MVP support on Windows and Linux. | GR-011 |
| SRS-NFR-002 | Logging and observability | Emit verbose lifecycle logs with runtime-configurable level and redaction. | GR-059 |
| SRS-NFR-003 | Architecture consistency | GUI/TUI use shared engine and MVC boundaries. | GR-026, GR-058 |
| SRS-NFR-004 | Testability | Unit tests for major components and simple e2e for critical flows. | GR-039 |
| SRS-NFR-005 | CI quality gates | Lint and tests required in CI quality pipeline. | GR-040 |
| SRS-NFR-006 | Concurrency behavior | Periodic scheduler must not block primary sequence execution path. | GR-020, GR-039 |

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
| SRS-TEST-008 | Enable one periodic task and run a sequence in parallel. | Periodic task continues to execute while sequence completes. |
| SRS-TEST-009 | Switch periodic task OFF during execution. | No new periodic iterations start after OFF is applied. |
| SRS-TEST-010 | Enable two periodic tasks with different intervals. | Both execute in parallel without blocking foreground sequence flow. |
| SRS-TEST-011 | Save invalid periodic interval (`interval_ms=0`). | Validation fails with `SRS-E-VAL-006`. |
| SRS-TEST-012 | Run with unknown task reference. | Run is blocked with `SRS-E-TASK-001`. |
| SRS-TEST-013 | Trigger receive timeout on a step. | Step fails with `SRS-E-TRN-003` and policy-applied run status. |
| SRS-TEST-014 | Fail count assertion (`assertion_count` mismatch). | Verification fails with `SRS-E-VER-002`. |

## 14. Traceability Map to General Requirements

| SRS Requirement IDs | GR IDs |
| --- | --- |
| SRS-FR-001..SRS-FR-004 | GR-019, GR-020, GR-025 |
| SRS-FR-005..SRS-FR-009 | GR-008, GR-019, GR-020, GR-030 |
| SRS-FR-010..SRS-FR-012 | GR-009, GR-022, GR-023, GR-028 |
| SRS-FR-013..SRS-FR-019 | GR-012, GR-020, GR-023, GR-025, GR-026, GR-031, GR-059 |
| SRS-UI-001..SRS-UI-008 | GR-012, GR-025, GR-026, GR-057 |
| SRS-NFR-001..SRS-NFR-006 | GR-011, GR-020, GR-039, GR-040, GR-058, GR-059 |

## 15. Open Items for Next Revision (v0.4)

1. Add measurable capacity/performance targets.
2. Add full test matrix and pass thresholds.
3. Add security-focused negative test scenarios (malformed payloads, oversized packets, invalid contract inputs).
