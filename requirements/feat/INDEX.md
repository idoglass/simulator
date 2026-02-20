# Feature Requirements Index (MVP-First Implementation Plan)

This index defines the recommended implementation order for the simulator.
The order is updated for the current stack and constraints:

- Python desktop application
- GUI via `py-gui` submodule (`tk-mvc`)
- TUI via Textual
- TCP + UDP in MVP
- Count-based verification in MVP
- File-based capture/replay

## A) Product Implementation Order (Build in this sequence)

| Order | Milestone | Feature File | Depends On | Why now | Status |
| --- | --- | --- | --- | --- | --- |
| 1 | MVP Core | [robust-generic-stateless-simulator.md](./robust-generic-stateless-simulator.md) | None | Establishes the core product boundary. | Done |
| 2 | MVP Core | [mvc-architecture-framework-compliance.md](./mvc-architecture-framework-compliance.md) | 1 | Locks framework and layering constraints before feature growth. | Done |
| 3 | MVP Core | [shared-simulation-engine-gui-tui.md](./shared-simulation-engine-gui-tui.md) | 1,2 | Prevents duplicated logic between GUI/TUI. | Done |
| 4 | MVP Core | [stateless-application-execution-boundary.md](./stateless-application-execution-boundary.md) | 1,3 | Enforces no hidden mutable run state. | Done |
| 5 | MVP Core | [target-based-simulation-execution.md](./target-based-simulation-execution.md) | 1,3,4 | Enables real target-driven runs. | Done |
| 6 | MVP Core | [udp-tcp-protocol-support.md](./udp-tcp-protocol-support.md) | 5 | Delivers required transport scope in MVP. | Done |
| 7 | MVP Core | [h-ctypes-message-structure-validation.md](./h-ctypes-message-structure-validation.md) | 5 | Locks message contract source-of-truth. | Done |
| 8 | MVP Core | [ctypes-and-registered-tasks-driven-simulation.md](./ctypes-and-registered-tasks-driven-simulation.md) | 5,7 | Restricts runtime behavior to approved inputs. | Done |
| 9 | MVP Core | [registered-task-only-execution.md](./registered-task-only-execution.md) | 8 | Prevents uncontrolled execution paths. | Done |
| 10 | MVP Core | [runtime-task-loading-registration.md](./runtime-task-loading-registration.md) | 8,9 | Adds extensibility without restart. | Done |
| 11 | MVP Core | [send-receive-message-simulation-scaling.md](./send-receive-message-simulation-scaling.md) | 6,8,10 | Provides core transport-flow behavior. | Done |
| 12 | MVP Core | [request-matching-and-verification.md](./request-matching-and-verification.md) | 11 | Adds measurable run correctness checks. | Done |
| 13 | MVP Core | [gui-and-tui-interfaces.md](./gui-and-tui-interfaces.md) | 3,11 | Exposes engine through both product interfaces. | Done |
| 14 | MVP Core | [core-simulation-capabilities-gui-tui.md](./core-simulation-capabilities-gui-tui.md) | 13 | Ensures minimum functional parity. | Done |
| 15 | MVP Core | [verbose-lifecycle-logging-redaction.md](./verbose-lifecycle-logging-redaction.md) | 11,12 | Enables diagnosability from first release. | Done |
| 16 | MVP Core | [critical-path-test-coverage.md](./critical-path-test-coverage.md) | 6-15 | Locks MVP quality and regression protection. | Done |
| 17 | MVP Hardening | [ci-quality-gates-lint-test-security.md](./ci-quality-gates-lint-test-security.md) | 16 | Automates quality enforcement in CI. | Done |
| 18 | MVP Hardening | [modular-code-ownership-boundaries.md](./modular-code-ownership-boundaries.md) | 2,3 | Improves maintainability and team velocity. | Done |
| 19 | MVP Hardening | [portability-compatibility-matrix.md](./portability-compatibility-matrix.md) | 6,13,16 | Validates Windows/Linux desktop targets. | Done |
| 20 | MVP Hardening | [gui-tui-help-man-documentation.md](./gui-tui-help-man-documentation.md) | 13,14 | Makes features usable without tribal knowledge. | Done |
| 21 | MVP Hardening | [prefer-reliable-third-party-libraries.md](./prefer-reliable-third-party-libraries.md) | 1-20 | Reduces custom-code risk and effort. | Done |
| 22 | Post-MVP | [multi-application-target-simulation-capacity.md](./multi-application-target-simulation-capacity.md) | 11,16 | Expand throughput after stable MVP baseline. | Done |
| 23 | Post-MVP | [task-composition-from-registered-tasks.md](./task-composition-from-registered-tasks.md) | 10 | Adds power-user extensibility. | Done |
| 24 | Post-MVP | [proxy-traffic-recording-and-replay.md](./proxy-traffic-recording-and-replay.md) | 11,12,15 | Adds advanced workflow acceleration. | Done |
| 25 | Post-MVP | [gui-tui-create-tasks.md](./gui-tui-create-tasks.md) | 13,14,10,23 | Load, compose, create tasks in GUI and TUI. | Done |

## B) Governance and Process Plan (run in parallel, required gates)

These are non-runtime requirements but must stay active during implementation.

| Order | Governance Feature File | Status |
| --- | --- | --- |
| 1 | [baseline-requirements-document.md](./baseline-requirements-document.md) | Active |
| 2 | [project-wide-architecture-quality-governance.md](./project-wide-architecture-quality-governance.md) | Active |
| 3 | [feature-requirements-baseline-alignment.md](./feature-requirements-baseline-alignment.md) | Active |
| 4 | [baseline-vs-detailed-spec-boundary.md](./baseline-vs-detailed-spec-boundary.md) | Active |
| 5 | [separate-feature-requirements-docs.md](./separate-feature-requirements-docs.md) | Active |
| 6 | [stable-requirement-id-governance.md](./stable-requirement-id-governance.md) | Active |
| 7 | [normative-requirement-language.md](./normative-requirement-language.md) | Active |
| 8 | [feature-to-baseline-requirement-mapping.md](./feature-to-baseline-requirement-mapping.md) | Active |
| 9 | [requirements-implementation-validation-traceability.md](./requirements-implementation-validation-traceability.md) | Active |
| 10 | [pre-implementation-architecture-artifacts.md](./pre-implementation-architecture-artifacts.md) | Active |
| 11 | [architecture-approval-gate-before-implementation.md](./architecture-approval-gate-before-implementation.md) | Active |
| 12 | [feature-spec-from-template.md](./feature-spec-from-template.md) | Active |
| 13 | [complete-feature-spec-content.md](./complete-feature-spec-content.md) | Active |
| 14 | [feature-approval-before-implementation.md](./feature-approval-before-implementation.md) | Active |

## C) Planning Notes

- If a plan item changes the `py-gui` submodule pointer, follow `../../skills/SUBMODULE_WORKFLOW.md`.
- Keep GUI/TUI parity as a blocking review criterion for MVP core items.
- Move items from `Planned` to `In Progress`/`Done` only when linked feature docs and tests are updated.

## D) Reference Documents

- [FEATURE_REQUIREMENTS_TEMPLATE.md](./FEATURE_REQUIREMENTS_TEMPLATE.md)
- [FEATURE_REQUIREMENTS_MASTER.md](./FEATURE_REQUIREMENTS_MASTER.md)
- [FEATURE_REQUIREMENTS_EXAMPLE_RUNTIME_TASK_LOADING.md](./FEATURE_REQUIREMENTS_EXAMPLE_RUNTIME_TASK_LOADING.md)
