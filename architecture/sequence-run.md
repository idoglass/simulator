# Sequence Diagram: Happy Path Run

This document describes the primary run path from user action to verification result.

## Sequence (Mermaid)

```mermaid
sequenceDiagram
  actor User
  participant UI as GUI/TUI Adapter
  participant WF as Run Workflow
  participant Contracts as Contract Adapter
  participant Tasks as Task Registry Adapter
  participant Transport as TCP/UDP Adapter
  participant Verify as Verification Adapter
  participant Log as Logging

  User->>UI: Start run (target, protocol, task)
  UI->>WF: run(target, protocol, task_id)
  WF->>Contracts: validate_contracts(target)
  Contracts-->>WF: contract_ok
  WF->>Tasks: resolve(task_id)
  Tasks-->>WF: task_definition
  WF->>Transport: execute_messages(target, protocol, task_definition)
  Transport-->>WF: observed_interactions
  WF->>Verify: verify_count_rules(expected, observed)
  Verify-->>WF: pass/fail + mismatch_details
  WF->>Log: emit run lifecycle logs
  WF-->>UI: run_result + verification_result
  UI-->>User: Display result
```

## Happy Path Notes

1. UI layer only forwards user intent and displays outputs.
2. Workflow orchestrates services/adapters.
3. Contracts and tasks are validated/resolved before transport execution.
4. Verification in MVP is count-based.
5. Logs are emitted with correlation identifiers and redaction.

## Requirement Mapping

- GR-019, GR-020, GR-022, GR-023, GR-026, GR-030, GR-031, GR-059
