# FR-GR-029

- Source GR ID: GR-029
- Priority: P0
- Status: Implemented

## Feature Requirement
Support recording message traffic through a file-based proxy/capture mode and replaying captured traffic in simulation runs.

## Acceptance Criteria
- Simulator provides a capture mode that records inbound/outbound traffic for a selected target/session.
- Captured traffic is persisted as files and can be replayed without manual re-entry of messages.
- Replay runs produce deterministic outputs when using the same capture input and task/version context.

## Implementation
- CaptureReplayPort and FileCaptureReplayAdapter (write_capture, read_capture); run workflow writes capture after each run when port wired. Capture schema v1 in .capture.json; replay via read_capture for future replay workflow.
