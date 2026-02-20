# DDS Supporting 01: UI Design (GUI and TUI)

## 1. Purpose

Define UI-layer behavior and parity rules for configuration, execution, monitoring, and periodic task controls.

## 2. UI Architecture Contract

- GUI and TUI call the same application services.
- No UI-specific simulation logic is allowed in view components.
- Both surfaces must expose equivalent core capabilities.

## 3. Primary UI Flows

1. CRUD flows
   - applications, targets, contracts, tasks, transports, messages, expectations, sequences
2. Run flow
   - select sequence -> run -> observe per-step and overall status
3. Periodic control flow
   - toggle task ON/OFF while run is active
4. Diagnostics flow
   - inspect error code, reason, affected entity/step

## 4. GUI Design Notes

- Entity management panels/forms for full CRUD.
- Real-time execution timeline panel.
- Periodic task switch control (enabled/disabled) per periodic-capable task.
- Runtime status widget showing interval, last run, failure streak.

## 5. TUI Design Notes

- Live run status pane with event stream.
- Immediate feedback line with task runtime state.

## 6. Parity Checklist

Both GUI and TUI must support:

- sequence execution
- response verification result view
- error-code visibility
- run summary access

## 7. Accessibility and Usability Baseline

- surface-level validation errors close to user input point
- long-running runs remain observable without blocking UI interaction
- status changes must be visible within one refresh cycle of the active UI loop
