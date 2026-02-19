# Sequence Diagram: Runtime Task Load / Register

This document describes the task-loading flow from user action to validated registration.

## Sequence (Mermaid)

```mermaid
sequenceDiagram
  actor User
  participant UI as GUI/TUI Adapter
  participant WF as Task Workflow
  participant Parser as Task Adapter
  participant Contracts as Contract Adapter
  participant Registry as Task Registry Adapter
  participant Log as Logging

  User->>UI: Load task file
  UI->>WF: load_task(file_path)
  WF->>Parser: parse_task_definition(file_path)
  Parser-->>WF: task_definition / parse_error

  alt parse_error
    WF->>Log: emit task_load_failed(parse_error)
    WF-->>UI: failure(parse_error)
  else parsed
    WF->>Contracts: validate_contract_refs(task_definition)
    Contracts-->>WF: validation_ok / validation_error

    alt validation_error
      WF->>Log: emit task_validation_failed(validation_error)
      WF-->>UI: failure(validation_error)
    else valid
      WF->>Registry: register_atomic(task_definition)
      Registry-->>WF: registered(task_id) / duplicate_or_conflict

      alt register_failed
        WF->>Log: emit task_register_failed(reason)
        WF-->>UI: failure(reason)
      else register_ok
        WF->>Log: emit task_registered(task_id)
        WF-->>UI: success(task_id)
      end
    end
  end
```

## Validation and Atomicity Notes

1. Registration MUST occur only after parse + contract validation succeed.
2. Registration is atomic per task file (no partial mutation on failure).
3. Duplicate/conflicting task IDs are rejected with deterministic error output.
4. Success response includes stable task identifier for subsequent execution.

## Requirement Mapping

- GR-023, GR-027, GR-028, GR-022, GR-059
