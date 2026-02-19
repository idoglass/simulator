# UI Adapters

UI adapters connect framework-specific UI code to shared simulator services.

- `gui/`: Tkinter MVC integration (`py-gui` / `tk-mvc`).
- `tui/`: Textual integration.

## Responsibilities

- Convert UI events/commands into service calls.
- Format service results for presentation.
- Keep UI-specific concerns out of domain logic.

## Non-responsibilities

- No core business rules.
- No protocol parsing/execution logic.
