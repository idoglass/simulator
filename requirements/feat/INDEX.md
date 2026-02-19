# Feature Requirements Index (MVP-First Implementation Order)

This index defines the recommended implementation order for the simulator.
The order prioritizes a usable MVP first, then hardening, then advanced capabilities.

## A) Product Implementation Order (Build in this sequence)

| Order | Milestone | Feature File | Why now |
| --- | --- | --- | --- |
| 1 | MVP Core | [robust-generic-stateless-simulator.md](./robust-generic-stateless-simulator.md) | Establishes core architecture baseline. |
| 2 | MVP Core | [stateless-application-execution-boundary.md](./stateless-application-execution-boundary.md) | Enforces stateless boundary early. |
| 3 | MVP Core | [target-based-simulation-execution.md](./target-based-simulation-execution.md) | Enables real target-driven runs. |
| 4 | MVP Core | [udp-tcp-protocol-support.md](./udp-tcp-protocol-support.md) | Provides required transport scope (TCP/UDP). |
| 5 | MVP Core | [h-ctypes-message-structure-validation.md](./h-ctypes-message-structure-validation.md) | Locks message contract source-of-truth. |
| 6 | MVP Core | [ctypes-and-registered-tasks-driven-simulation.md](./ctypes-and-registered-tasks-driven-simulation.md) | Connects engine behavior to definitions/tasks only. |
| 7 | MVP Core | [registered-task-only-execution.md](./registered-task-only-execution.md) | Prevents uncontrolled execution paths. |
| 8 | MVP Core | [runtime-task-loading-registration.md](./runtime-task-loading-registration.md) | Delivers extensibility without restart. |
| 9 | MVP Core | [send-receive-message-simulation-scaling.md](./send-receive-message-simulation-scaling.md) | Provides working message flow behavior. |
| 10 | MVP Core | [request-matching-and-verification.md](./request-matching-and-verification.md) | Adds correctness checks for interactions. |
| 11 | MVP Core | [gui-and-tui-interfaces.md](./gui-and-tui-interfaces.md) | Exposes product to end users in both modes. |
| 12 | MVP Core | [core-simulation-capabilities-gui-tui.md](./core-simulation-capabilities-gui-tui.md) | Ensures minimum functional parity. |
| 13 | MVP Core | [shared-simulation-engine-gui-tui.md](./shared-simulation-engine-gui-tui.md) | Avoids drift and duplicate logic. |
| 14 | MVP Core | [verbose-lifecycle-logging-redaction.md](./verbose-lifecycle-logging-redaction.md) | Enables diagnosability from first release. |
| 15 | MVP Core | [critical-path-test-coverage.md](./critical-path-test-coverage.md) | Locks MVP quality and regression protection. |
| 16 | MVP Hardening | [mvc-architecture-framework-compliance.md](./mvc-architecture-framework-compliance.md) | Aligns code with intended architecture style. |
| 17 | MVP Hardening | [modular-code-ownership-boundaries.md](./modular-code-ownership-boundaries.md) | Improves maintainability and team velocity. |
| 18 | MVP Hardening | [ci-quality-gates-lint-test-security.md](./ci-quality-gates-lint-test-security.md) | Automates quality enforcement. |
| 19 | MVP Hardening | [portability-compatibility-matrix.md](./portability-compatibility-matrix.md) | Verifies PC compatibility targets. |
| 20 | MVP Hardening | [gui-tui-help-man-documentation.md](./gui-tui-help-man-documentation.md) | Makes features usable without tribal knowledge. |
| 21 | MVP Hardening | [prefer-reliable-third-party-libraries.md](./prefer-reliable-third-party-libraries.md) | Reduces custom-code risk and effort. |
| 22 | Post-MVP | [multi-application-target-simulation-capacity.md](./multi-application-target-simulation-capacity.md) | Expand capacity after stable MVP baseline. |
| 23 | Post-MVP | [task-composition-from-registered-tasks.md](./task-composition-from-registered-tasks.md) | Adds power-user extensibility. |
| 24 | Post-MVP | [proxy-traffic-recording-and-replay.md](./proxy-traffic-recording-and-replay.md) | Adds advanced workflow acceleration. |

## B) Governance and Process Order (run in parallel, required gates)

These are non-runtime requirements but must be kept active during implementation:

1. [baseline-requirements-document.md](./baseline-requirements-document.md)  
2. [project-wide-architecture-quality-governance.md](./project-wide-architecture-quality-governance.md)  
3. [feature-requirements-baseline-alignment.md](./feature-requirements-baseline-alignment.md)  
4. [baseline-vs-detailed-spec-boundary.md](./baseline-vs-detailed-spec-boundary.md)  
5. [separate-feature-requirements-docs.md](./separate-feature-requirements-docs.md)  
6. [stable-requirement-id-governance.md](./stable-requirement-id-governance.md)  
7. [normative-requirement-language.md](./normative-requirement-language.md)  
8. [feature-to-baseline-requirement-mapping.md](./feature-to-baseline-requirement-mapping.md)  
9. [requirements-implementation-validation-traceability.md](./requirements-implementation-validation-traceability.md)  
10. [pre-implementation-architecture-artifacts.md](./pre-implementation-architecture-artifacts.md)  
11. [architecture-approval-gate-before-implementation.md](./architecture-approval-gate-before-implementation.md)  
12. [feature-spec-from-template.md](./feature-spec-from-template.md)  
13. [complete-feature-spec-content.md](./complete-feature-spec-content.md)  
14. [feature-approval-before-implementation.md](./feature-approval-before-implementation.md)  

## C) Reference Documents

- [FEATURE_REQUIREMENTS_TEMPLATE.md](./FEATURE_REQUIREMENTS_TEMPLATE.md)
- [FEATURE_REQUIREMENTS_MASTER.md](./FEATURE_REQUIREMENTS_MASTER.md)
- [FEATURE_REQUIREMENTS_EXAMPLE_RUNTIME_TASK_LOADING.md](./FEATURE_REQUIREMENTS_EXAMPLE_RUNTIME_TASK_LOADING.md)
