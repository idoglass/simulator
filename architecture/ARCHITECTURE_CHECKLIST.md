# Architecture Design Stage Checklist

Use this checklist to complete architecture design **before implementation**.

## Exit Condition

Architecture design stage is complete only when:

1. All **Required** items below are marked Done.
2. Each Done item has a linked artifact file/path.
3. Open risks and ADR decisions are documented.

## Checklist (Required)

| ID | Item | Required Artifacts | Requirement Mapping | Done Criteria | Status |
| --- | --- | --- | --- | --- | --- |
| A-01 | System context definition | `architecture/context-diagram.md` | GR-044, GR-045 | External actors, boundaries, and submodule role (`py-gui`) are explicit. | Done |
| A-02 | Component architecture | `architecture/component-diagram.md` | GR-044, GR-058 | Components and dependency direction are defined (`domain -> ports <- adapters`). | Done |
| A-03 | Runtime sequence (happy path) | `architecture/sequence-run.md` | GR-019, GR-020, GR-023, GR-026 | End-to-end run flow from target selection to result is documented. | Done |
| A-04 | Runtime sequence (task load) | `architecture/sequence-task-load.md` | GR-027, GR-028 | Runtime task load/register flow and validation points are documented. | Done |
| A-05 | Runtime sequence (capture/replay) | `architecture/sequence-capture-replay.md` | GR-029 | File-based capture and replay flow is documented and deterministic assumptions listed. | Done |
| A-06 | Domain model | `architecture/domain-model.md` | GR-021, GR-023, GR-030 | Core entities and lifecycle states are defined, including stateless boundary notes. | Done |
| A-07 | Event model + event manager plan | `architecture/event-model.md` | GR-058, GR-059 | Event types, publish/subscribe points, and placement (`ports` + implementation) are defined. | Done |
| A-08 | Port contracts (interfaces) | `architecture/port-contracts.md` | GR-022, GR-023, GR-026, GR-031 | Interface definitions exist for transport, contracts, tasks, verification, capture/replay, events. | Done |
| A-09 | Contract mapping rules (`.h` -> `ctypes`) | `architecture/contract-mapping.md` | GR-009, GR-022 | Mapping/validation rules, unsupported constructs, and error behavior are documented. | Done |
| A-10 | Task format decision and versioning | `architecture/task-format.md` | GR-027, GR-028 | Task format chosen (JSON/YAML/other), schema versioning and compatibility rules defined. | Todo |
| A-11 | Protocol behavior spec (TCP/UDP) | `architecture/transport-spec.md` | GR-031 | Client/server behavior, timeout/retry, error semantics, and framing assumptions are defined. | Todo |
| A-12 | Verification spec (MVP count-based) | `architecture/verification-spec.md` | GR-030 | Count-based rules, pass/fail conditions, and mismatch reporting format are defined. | Todo |
| A-13 | Configuration model | `architecture/config-model.md` | GR-011, GR-031 | Runtime config schema and per-target/per-run overrides are defined and validated. | Todo |
| A-14 | Observability and redaction spec | `architecture/logging-observability.md` | GR-057, GR-059 | Required logs, fields, IDs, and redaction policy are defined. | Todo |
| A-15 | Test architecture plan | `architecture/test-strategy.md` | GR-039, GR-040 | Unit/integration/simple e2e scope and Windows/Linux validation plan are defined. | Todo |
| A-16 | Risk register | `architecture/risk-register.md` | GR-044 | Top risks, impact, mitigation, and owners are documented. | Todo |
| A-17 | ADR set for major decisions | `architecture/adr/ADR-*.md` | GR-044, GR-045 | Key decisions have ADRs (accepted/rejected options + rationale). | Todo |

## Checklist (Recommended)

| ID | Item | Artifact | Done Criteria | Status |
| --- | --- | --- | --- | --- |
| R-01 | Error code catalog | `architecture/error-codes.md` | Error families and user-facing messages are standardized. | Todo |
| R-02 | Dependency policy | `architecture/dependency-policy.md` | Library selection/security/license rules are explicit. | Todo |
| R-03 | Performance budget | `architecture/performance-budget.md` | Initial latency/throughput targets and measurement approach are defined. | Todo |

## Governance Notes

- Keep this checklist aligned with:
  - `requirements/GENERAL_REQUIREMENTS.md`
  - `requirements/feat/pre-implementation-architecture-artifacts.md`
  - `requirements/feat/architecture-approval-gate-before-implementation.md`
- If architecture affects GUI framework integration, follow:
  - `skills/SUBMODULE_WORKFLOW.md`
