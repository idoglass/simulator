# Simulator help content (GUI Help / TUI man)

User-facing help for simulator capabilities. Expose via GUI Help menu and TUI help screen.

## Commands
- **Run** – Execute a simulation run (target, task, protocol). Default: default-target, ping-smoke, tcp.
- **List tasks** – Show registered tasks (loaded from fixtures or loaded/composed/created at runtime).
- **Load task** – Register a task from a .task.json file path (runtime, no restart).
- **Compose** – Create a new task from two or more registered base tasks; new task is registered.
- **Create task** – Create a new task from scratch (task_id, name, steps); registered immediately.

## Requirements
- GR-057: User-facing documentation exposed through GUI Help and TUI help/man.
