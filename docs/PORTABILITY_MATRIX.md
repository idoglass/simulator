# Portability and compatibility matrix (FR-GR-011)

MVP supports Windows and Linux desktop. This matrix is validated for simulator runs.

| OS       | Architecture | Python   | Status  |
|----------|--------------|----------|---------|
| linux    | x86_64       | 3.11+    | Supported |
| windows  | x86_64       | 3.11+    | Supported |

## Runtime expectations
- GUI: Tkinter available (e.g. `python3-tk` on Debian/Ubuntu).
- TUI: Textual optional; terminal with UTF-8.
- TCP/UDP: Standard library socket support.

## CI
- Pipeline runs on ubuntu-latest and windows-latest; tests and boundary checks run on both.
