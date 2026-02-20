# Architecture Conformance Checklist for PRs

Use this checklist in every implementation PR to prove conformance with approved architecture.

## 1) Required Mapping

1. List changed source areas (for example `src/simulator/domain/services`, `adapters/transport/tcp`).
2. Map each changed area to one or more architecture artifacts.
3. Map each changed area to relevant GR IDs.
4. State whether any accepted ADR is impacted.

## 2) Mapping Template

| Changed Area | Architecture Artifact(s) | Requirement ID(s) | ADR Impact | Notes |
| --- | --- | --- | --- | --- |
| `src/simulator/...` | `architecture/<artifact>.md` | `GR-xxx` | `None` or `ADR-xxx` | rationale |

## 3) Conformance Checks (Required)

- [ ] Domain logic does not depend directly on UI/framework modules.
- [ ] UI adapters do not embed core business logic.
- [ ] Transport execution remains off UI thread/event loop.
- [ ] Config behavior respects precedence and validation rules.
- [ ] Verification behavior remains deterministic for identical inputs.
- [ ] Logging/redaction requirements are preserved.
- [ ] If behavior changed materially, ADR update/addition is included.

## 4) Evidence to Include in PR

1. Relevant test evidence (unit/integration/e2e) for changed architecture boundaries.
2. Links to updated architecture docs when behavior/contracts changed.
3. Explicit note when no architecture artifact changes are needed (with rationale).

## 5) Escalation Rule

If a change cannot be mapped to current architecture artifacts, do not merge until:

1. architecture artifact is updated, and
2. decision is recorded in existing or new ADR.
