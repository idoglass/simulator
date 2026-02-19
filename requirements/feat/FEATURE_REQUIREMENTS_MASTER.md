# Master Feature Requirements (Derived from General Requirements)

This document creates one feature requirement entry for each general requirement in `../GENERAL_REQUIREMENTS.md`.

| FR ID | Source GR ID | Feature Requirement | Acceptance Criteria | Priority |
| --- | --- | --- | --- | --- |
| FR-GR-001 | GR-001 | Keep an enforceable baseline requirements document in repository scope. | `requirements/GENERAL_REQUIREMENTS.md` exists and is used as baseline reference in feature specs. | P0 |
| FR-GR-002 | GR-002 | Enforce that each feature requirement document aligns to baseline rules. | Every feature requirement doc includes mapped GR IDs and no unapproved conflicts. | P0 |
| FR-GR-003 | GR-003 | Standardize normative terms usage (`SHALL/MUST`, `SHOULD`, `MAY`). | Requirement docs use normative keywords consistently and definitions are present. | P1 |
| FR-GR-013 | GR-013 | Preserve stable requirement IDs across edits. | Existing GR IDs are not renumbered on revisions; non-sequential IDs are accepted. | P1 |
| FR-GR-004 | GR-004 | Define project-wide architecture, reliability, security, testing, and governance requirements. | Feature specs reference architecture/NFR/governance constraints where applicable. | P0 |
| FR-GR-005 | GR-005 | Maintain separate feature-specific requirements per feature. | Each implemented feature has its own requirements file under `requirements/feat/`. | P0 |
| FR-GR-006 | GR-006 | Keep detailed UX/schema/payload/sprint planning out of baseline doc. | Detailed implementation details are documented only in feature-specific docs. | P1 |
| FR-GR-007 | GR-007 | Deliver robust generic stateless simulator foundation. | Core simulator runs target flows without coupling to one specific application model. | P0 |
| FR-GR-008 | GR-008 | Support simulation of one or more applications per target up to validated limits. | Capacity limits are configured and tested; simulator processes multi-application message flows. | P0 |
| FR-GR-009 | GR-009 | Drive simulation from `.h`/`ctypes` definitions plus registered tasks only. | Runs fail validation when message/task definitions are outside allowed sources. | P0 |
| FR-GR-010 | GR-010 | Maintain traceability from requirements to implementation and validation artifacts. | Feature docs, commits, and tests include requirement mapping references. | P1 |
| FR-GR-011 | GR-011 | Provide explicit portability compatibility matrix support. | Feature docs include OS/arch/runtime matrix and portability validation status. | P0 |
| FR-GR-012 | GR-012 | Provide both GUI and TUI interfaces for simulator usage. | Feature behavior is available via both GUI and TUI entry points. | P0 |
| FR-GR-019 | GR-019 | Accept target input and execute simulation flow for that target. | Simulation run requires target input and executes against selected target context. | P0 |
| FR-GR-020 | GR-020 | Simulate send/receive message behavior with resource-bound scaling. | Multi-application message flows execute correctly within configured limits. | P0 |
| FR-GR-021 | GR-021 | Enforce stateless execution boundary at application layer. | No mutable per-session/per-target state persists in process between requests. | P0 |
| FR-GR-022 | GR-022 | Use `.h`/`ctypes` metadata for message structures/participants/flow rules. | Invalid type/field references are rejected during validation. | P0 |
| FR-GR-023 | GR-023 | Execute simulation actions only through registered tasks. | Engine rejects non-registered task execution requests. | P0 |
| FR-GR-024 | GR-024 | Map feature requirements to Section 6/7 baseline requirements. | Each feature requirement item has mapped GR ID references. | P1 |
| FR-GR-025 | GR-025 | Expose core simulation capabilities in both GUI and TUI. | Equivalent core operations are accessible in both interfaces. | P0 |
| FR-GR-026 | GR-026 | Use one shared simulation engine for GUI and TUI. | GUI and TUI call shared engine/service APIs and produce equivalent results. | P0 |
| FR-GR-027 | GR-027 | Support creation of user-defined tasks from existing registered tasks. | Task composition flow creates valid reusable tasks with unique task IDs. | P0 |
| FR-GR-028 | GR-028 | Support runtime task loading and registration before execution. | New task definitions can be loaded, validated, and executed without restart. | P0 |
| FR-GR-038 | GR-038 | Keep code modular with clear ownership boundaries. | Modules and interfaces are documented; cross-module dependencies remain controlled. | P1 |
| FR-GR-039 | GR-039 | Cover critical paths with unit/integration/end-to-end tests. | Required test suites exist and pass for feature-critical workflows. | P0 |
| FR-GR-040 | GR-040 | Enforce CI/CD gates for lint, tests, and security checks. | CI fails when lint/tests/security checks fail. | P0 |
| FR-GR-057 | GR-057 | Publish user-facing UI docs via GUI Help and TUI help/man. | Feature usage appears in GUI help and TUI help/man with current examples. | P0 |
| FR-GR-058 | GR-058 | Implement features under MVC architecture and designated FW constraints. | Feature design maps to MVC layers and follows framework standards. | P0 |
| FR-GR-059 | GR-059 | Emit verbose lifecycle logs with configurable levels and redaction. | Required events are logged; log level is configurable; sensitive values are redacted. | P0 |
| FR-GR-060 | GR-060 | Prefer reliable/common third-party libraries when suitable. | Library decision includes security/maintenance/license check; custom code is justified when selected. | P1 |
| FR-GR-044 | GR-044 | Produce required architecture artifacts before implementation. | Feature references architecture artifacts (diagram/data/interface/deploy/risk/ADR) before coding starts. | P0 |
| FR-GR-045 | GR-045 | Block implementation until required architecture artifacts are approved. | Feature implementation status remains "not started" until documented approvals exist. | P0 |
| FR-GR-054 | GR-054 | Create dedicated feature requirements from template for every feature. | New features include a file derived from `FEATURE_REQUIREMENTS_TEMPLATE.md`. | P0 |
| FR-GR-055 | GR-055 | Include stories, acceptance criteria, API/data needs, NFRs, and tests in feature docs. | Feature document contains all required sections with concrete values. | P0 |
| FR-GR-056 | GR-056 | Require feature requirement review/approval before implementation begins. | Feature implementation starts only after approval status is set in feature doc. | P0 |

