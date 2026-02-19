# Skills Package for Simulator Projects

This folder defines generic engineering skills for message-simulation tools like this project:

- stateless simulation engine
- `.h` / `ctypes`-driven message structures
- runtime task registration/composition
- GUI + TUI parity
- TCP/UDP transport support
- capture/replay and interaction verification

Project-specific context now includes the `py-gui` submodule (`tk-mvc` framework) located at:

- `../py-gui`

## Files

- `GENERIC_SKILLS_FOR_SIMULATOR_PROJECT.md`  
  Core skill matrix by area, expected outcomes, and common mistakes.

- `CODE_SMELL_AND_OOP_CHECKLIST.md`  
  OOP design quality checklist plus code smell detection/remediation guidance.

- `PROJECT_DISCOVERY_QUESTIONS.md`  
  Questions to tailor these generic skills to your exact implementation stack and constraints.

- `PROJECT_DISCOVERY_ANSWERS.md`  
  Captured project decisions and current open items.

- `PROJECT_SKILLS_STANDARD_V1.md`  
  Project-specific skills standard derived from discovery answers.

## How to use

1. Start with `GENERIC_SKILLS_FOR_SIMULATOR_PROJECT.md` to align team expectations.
2. Use `CODE_SMELL_AND_OOP_CHECKLIST.md` during design reviews and PR reviews.
3. Answer `PROJECT_DISCOVERY_QUESTIONS.md`; record decisions in `PROJECT_DISCOVERY_ANSWERS.md`.
4. Follow `PROJECT_SKILLS_STANDARD_V1.md` as the default implementation/review baseline for this project.
