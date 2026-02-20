# Sequence Diagram: File-Based Capture and Replay

This document describes file-based traffic capture and replay in MVP.

## Sequence (Mermaid)

```mermaid
sequenceDiagram
  actor User
  participant UI as GUI/TUI Adapter
  participant WF as Run/Capture Workflow
  participant Transport as TCP/UDP Adapter
  participant Capture as Capture/Replay Adapter
  participant Verify as Verification Adapter
  participant Log as Logging

  User->>UI: Start capture run (target, protocol, task)
  UI->>WF: run_with_capture(config)
  WF->>Transport: execute_messages(config)
  Transport-->>WF: observed_interactions
  WF->>Capture: write_capture_file(observed, metadata)
  Capture-->>WF: capture_file_path
  WF->>Verify: verify_count_rules(expected, observed)
  Verify-->>WF: pass/fail
  WF->>Log: emit capture_run_completed(run_id, capture_file_path)
  WF-->>UI: capture_result + verification_result

  User->>UI: Replay from capture file
  UI->>WF: replay(capture_file_path)
  WF->>Capture: read_capture_file(capture_file_path)
  Capture-->>WF: replay_input + metadata
  WF->>Transport: replay_messages(replay_input, metadata.protocol)
  Transport-->>WF: replay_observed
  WF->>Verify: verify_count_rules(expected_from_metadata, replay_observed)
  Verify-->>WF: pass/fail + mismatch_details
  WF->>Log: emit replay_completed(run_id)
  WF-->>UI: replay_result + verification_result
```

## Determinism Assumptions (MVP)

1. Capture artifacts persist as files and include replay-critical metadata:
   - protocol
   - target identifier
   - task/version context
   - timestamp/run ID
2. Replay uses the same message order from capture input.
3. For deterministic comparison, expected verification rules are loaded from capture metadata or run config.
4. Non-deterministic external effects are out of scope for MVP and should be documented per feature.

## Requirement Mapping

- GR-029, GR-030, GR-031, GR-059

## Related Artifact

- `architecture/capture-schema-versioning.md`
