# FR-GR-029

- Source GR ID: GR-029
- Priority: P0
- Status: Draft

## Feature Requirement
Support recording message traffic through a proxy/capture mode and replaying captured traffic in simulation runs.

## Acceptance Criteria
- Simulator provides a capture mode that records inbound/outbound traffic for a selected target/session.
- Captured traffic can be replayed without manual re-entry of messages.
- Replay runs produce deterministic outputs when using the same capture input and task/version context.
