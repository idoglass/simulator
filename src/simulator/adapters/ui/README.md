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

## ToDo
- main loop:
  1. ask user to select target (from list)
  2. ask user to select what task to run
  4. run task and show user the results
  5. return to 1
 
- if user run simulator on tui mode
  1. if no argument run main loop
  2. if --list or -l with out parameters list all list able objects and let the user choose 
     - task
     - contracts
     - scenario
     - target
  3. if --list <param> or -l <param> with parameter show the list
  4. if --task <TASK_NAME> or -t <TASK_NAME> skip select task from main loop but run it
  5. if --targrt <TARGET_NAME> or -T <TARGET_NAME> skip select target from main loop but run it
  6. if -scenario <SENARIO_NAME> or -s <SENARIO_NAME> run scenario and show results  
