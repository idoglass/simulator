# General Project Requirements

## 1. Purpose

- **GR-001:** This document SHALL define mandatory baseline project requirements that govern architecture and delivery before implementation.
- **GR-002:** All feature-specific requirement documents SHALL comply with this baseline unless an exception is explicitly approved by the technical lead and product owner.
- **GR-003:** The terms **SHALL/MUST**, **SHOULD**, and **MAY** are normative. SHALL/MUST indicates a mandatory requirement.
- **GR-013:** Requirement IDs in this document SHALL remain stable across revisions and MAY be non-sequential.

## 2. Scope of This Document

- **GR-004:** This document SHALL define project-wide requirements for architecture, security, reliability, operations, testing, and governance.
- **GR-005:** This document SHALL NOT replace feature-specific requirements; each feature SHALL have its own requirement document.
- **GR-006:** Detailed UX behavior, field-level schema definitions, low-level API payload contracts, and sprint task decomposition SHALL be defined in feature-specific documents.

## 3. Project Goals

- **GR-007:** The project SHALL deliver a robust and generic stateless application.
- **GR-008:** The application SHALL simulate, for a target, one or more applications by sending and receiving messages, up to configured and validated capacity limits.
- **GR-009:** Simulation behavior SHALL be driven only by C type definitions (`ctypes`) from `.h` files and registered tasks (built-in or user-defined).
- **GR-010:** Requirements, implementation, and validation artifacts SHALL remain traceable end-to-end.
- **GR-011:** The simulator SHALL be portable across supported target environments defined by an explicit compatibility matrix (OS, architecture, and runtime/toolchain versions).
- **GR-012:** The simulator SHALL provide both a graphical user interface (GUI) and a terminal user interface (TUI).

## 6. Functional Requirement Categories (High-Level)

- **GR-019:** The application SHALL receive a target and execute simulation flows for that target.
- **GR-020:** The application SHALL simulate message send/receive behavior across one or more applications, constrained by configured and validated resource limits.
- **GR-021:** The application SHALL remain stateless at the application layer during simulation execution and SHALL NOT persist mutable per-session or per-target execution state in process between requests.
- **GR-022:** The application SHALL use only C type definitions (`ctypes`) from `.h` files to define message structures, participants, and simulation flow rules.
- **GR-023:** The application SHALL execute simulation behavior only through registered tasks.
- **GR-024:** Feature-specific requirements SHALL map to one or more requirements in this section or Section 7.
- **GR-025:** GUI and TUI interfaces SHALL expose the core simulation capabilities.
- **GR-026:** GUI and TUI interfaces SHALL use the same underlying simulation engine and requirement model.
- **GR-027:** The simulator SHALL provide a way to create user-defined tasks by composing or extending existing registered tasks.
- **GR-028:** The simulator SHALL support loading and registering tasks at runtime prior to execution.

## 7. Non-Functional Requirements

### 7.5 Maintainability and Testability

- **GR-038:** The codebase SHALL be modular with clear ownership boundaries.
- **GR-039:** Automated testing SHALL include unit, integration, and end-to-end coverage for critical paths.
- **GR-040:** CI/CD quality gates SHALL include linting, test execution, and security checks.

### 7.6 Architecture, Documentation, and Logging Standards

- **GR-057:** User-facing documentation for all UI capabilities SHALL be exposed through the GUI Help section and the TUI help/man section; relevant developer notes MAY be promoted from code comments after documentation review.
- **GR-058:** The architecture SHALL follow the MVC pattern and use the designated framework (FW), with detailed framework standards defined in a separate architecture specification.
- **GR-059:** The application SHALL provide highly verbose logs for key lifecycle events (including simulation start/stop, task creation/loading, and message send/receive), with runtime-configurable log levels and mandatory redaction of sensitive data.
- **GR-060:** When a reliable and commonly adopted third-party library is available and suitable, it SHALL be preferred over custom implementation, provided it meets security, maintenance, and license-compatibility requirements.

## 8. Architecture Definition Requirements

- **GR-044:** Before implementation starts, the following artifacts SHALL be produced and reviewed:
  1. Context and component architecture diagrams
  2. Data model and data flow overview
  3. Integration interface inventory (APIs/events/files)
  4. Deployment topology and environment strategy
  5. Risk register with mitigations and owners
  6. Architecture Decision Records (ADRs) for major tradeoffs
- **GR-045:** Implementation SHALL NOT begin until the artifacts above are approved by the designated decision owners.

## 12. Next Step

- **GR-054:** Each feature SHALL have a dedicated requirements document based on `feat/FEATURE_REQUIREMENTS_TEMPLATE.md`.
- **GR-055:** Feature requirements SHALL include user stories, acceptance criteria, API/data contract requirements, measurable NFR targets, and mapped test scenarios.
- **GR-056:** Feature implementation SHALL begin only after feature requirements are reviewed and approved.
