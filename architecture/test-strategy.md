# Test Strategy (Architecture-Level)

This document defines the architecture-driven test plan for unit, integration, and simple end-to-end validation.

## 1) Scope

- Covers shared simulation engine, domain/services, ports/adapters, and GUI/TUI integration boundaries.
- Applies to MVP platform targets: Windows and Linux.
- Aligns test strategy to architecture artifacts before implementation starts.

## 2) Test Principles

1. Test behavior at architectural boundaries, not only internal helpers.
2. Prefer deterministic tests with fixed fixtures and stable timing assumptions.
3. Keep protocol/network tests isolated and reproducible (loopback and controlled ports).
4. Ensure both GUI and TUI paths use the same core engine behavior.

## 3) Test Pyramid and Ownership

### 3.1 Unit Tests (Primary Volume)

Targets:

- domain models and services
- rule evaluation (verification count-based behavior)
- config resolution and validation logic
- task parser/validator normalization logic

Expectations:

- fast execution
- no real network or UI dependencies
- extensive negative-path coverage for validation errors

### 3.2 Integration Tests (Boundary Confidence)

Targets:

- transport adapters (TCP/UDP client/server happy paths + timeout/retry failures)
- contract loader pipeline (`.h` and `ctypes` entry paths)
- task runtime loading + atomic registration
- capture write/read + replay flow correctness
- structured logging field propagation and redaction

Expectations:

- controlled environment with deterministic fixtures
- explicit setup/teardown for sockets/files

### 3.3 End-to-End Smoke Tests (Critical Workflows)

Targets:

- GUI run start -> result display (smoke)
- TUI run start -> result display (smoke)
- capture + replay critical path

Expectations:

- simple critical path, not exhaustive UI automation
- run in CI where runtime prerequisites are available
- graceful skip behavior where GUI prerequisites are unavailable

## 4) Cross-Platform Validation Matrix

MVP matrix:

- Linux: required
- Windows: required

Each matrix run must execute:

1. unit suite
2. integration subset (transport/config/verification/task)
3. GUI/TUI smoke checks (or documented skip with reason where environment lacks prerequisites)

## 5) Requirement Traceability

Tests must map to requirement IDs and architecture artifacts:

- GR-031 -> transport tests
- GR-030 -> verification tests
- GR-027/GR-028 -> task loading and composition tests
- GR-011 -> compatibility/config tests
- GR-059 -> logging + redaction tests

Traceability artifacts:

- test case naming convention includes requirement IDs
- CI summaries include per-requirement pass/fail status where feasible

## 6) Non-Functional Test Focus

1. Determinism: repeated identical inputs produce identical verification outcomes.
2. Robustness: malformed config/task/contract inputs fail with deterministic codes.
3. Responsiveness: transport operations do not block UI event loops.
4. Observability: required fields/correlation IDs exist in logs.

## 7) Fixtures and Test Data

1. Maintain stable contract fixtures (`.h` + generated `ctypes` samples).
2. Maintain canonical task fixtures for valid and invalid cases.
3. Maintain transport payload fixtures per protocol.
4. Maintain capture artifacts for replay determinism tests.

## 8) CI Gating Plan

Required CI gates:

1. requirements/doc validation
2. lint checks
3. unit tests
4. integration tests (selected deterministic subset)
5. GUI/TUI smoke checks
6. submodule policy checks

Failure policy:

- Any required gate failure blocks merge.

## 9) Known Testing Risks and Mitigations

1. Environment differences across OS runners -> use explicit compatibility checks and controlled dependencies.
2. Flaky socket timing tests -> use deterministic timeouts, bounded retries, and loopback-only integration paths.
3. GUI runner limitations in CI -> keep smoke scope minimal and support explicit skip conditions with audit logs.

## 10) Requirement Mapping

- GR-039, GR-040, GR-011, GR-026, GR-031
