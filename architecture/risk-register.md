# Architecture Risk Register (MVP)

This register tracks top architecture/design risks, impact, mitigation, ownership, and status.

## 1) Risk Scale

- **Impact:** Low / Medium / High
- **Likelihood:** Low / Medium / High
- **Priority:** derived from impact + likelihood

## 2) Risks

| Risk ID | Risk | Impact | Likelihood | Priority | Mitigation | Owner | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| RISK-001 | Divergence between `.h` input parsing and generated `ctypes` input behavior causes inconsistent contracts. | High | Medium | High | Enforce single canonical normalization/validation pipeline; add parity tests for both entry paths. | Contracts lead | Open |
| RISK-002 | Transport behavior differences between TCP/UDP modes lead to nondeterministic verification outcomes. | High | Medium | High | Define strict transport semantics and deterministic timeout/retry policy; add protocol matrix tests. | Transport lead | Open |
| RISK-003 | UI responsiveness degrades if transport/event handling blocks UI loop. | High | Medium | High | Enforce off-UI transport execution and UI-thread marshalling; add responsiveness tests. | App architecture owner | Open |
| RISK-004 | Runtime task loading introduces invalid or unsafe task definitions. | High | Medium | High | Strict schema validation, deterministic error reporting, and atomic registration with rollback. | Task subsystem owner | Open |
| RISK-005 | Count-based MVP verification is insufficient for sequence-sensitive real scenarios. | Medium | High | High | Document MVP limitation; roadmap sequence/state assertions post-MVP; ensure clear mismatch reporting. | Verification owner | Open |
| RISK-006 | File-based capture artifacts become too large and degrade replay performance. | Medium | Medium | Medium | Add capture size controls, metadata indexing, and bounded diagnostics sampling. | Capture/replay owner | Open |
| RISK-007 | Logging verbosity leaks sensitive data despite redaction intent. | High | Medium | High | Mandatory redaction policy, tests for secret masking, and review checklist for new log fields. | Observability owner | Open |
| RISK-008 | Cross-platform inconsistencies (Windows/Linux) break portability guarantees. | High | Medium | High | Maintain explicit compatibility matrix and enforce platform CI runs for required suites. | Release/CI owner | Open |
| RISK-009 | Submodule drift (`py-gui`) breaks GUI integration unexpectedly. | Medium | Medium | Medium | Follow submodule workflow, pin updates, and run GUI smoke checks before merge. | GUI integration owner | Open |
| RISK-010 | Architecture docs drift from implementation over time. | Medium | High | High | Add architecture conformance checklist to PR workflow and periodic architecture review gate. | Tech lead | Open |

## 3) Review Cadence

1. Review risk register at each architecture milestone and release cut.
2. Update status after mitigation implementation or residual-risk acceptance.
3. Escalate all High-priority unresolved risks in architecture approval review.

## 4) Residual Risk Policy

- High residual risks require explicit approval from designated decision owners.
- Deferred mitigations must include owner and target milestone.

## 5) Requirement Mapping

- GR-044, GR-045, GR-039, GR-059
