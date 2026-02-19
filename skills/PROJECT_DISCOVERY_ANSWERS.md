# Project Discovery Answers (Current)

## Confirmed

1. Primary language: **Python**
2. GUI framework direction: **Tkinter-based MVC framework** via `py-gui` submodule (`tk-mvc`)
3. TUI framework: **Textual**
4. Runtime mode: **Desktop app**
5. TCP/UDP MVP scope: **Both client and server modes**
6. TLS in MVP: **No**
7. `.h` input source: **Repository and/or external files**
8. Task definition format: **TBD**
9. Verification depth in MVP: **Count-based verification**
10. Capture/replay mode: **File-based**
11. Testing expectation: **Unit tests for all major parts + simple e2e**
12. MVP OS targets: **Windows + Linux**

## Open Items

- Task definition format decision (JSON, YAML, other).

## Framework Reference (Resolved)

- Submodule path: `../py-gui`
- Upstream URL: `https://github.com/idoglass/py-gui.git`
- Framework package: `tk-mvc` (Python 3.11+)
- Key framework capabilities used for this project:
  - MVC base classes and binding helpers
  - App lifecycle and DI entry points
  - Task protocol, TaskRegistry, TaskRunner, Scheduler, dynamic task loader
  - CLI scaffolding/build helpers
