# Prefer reliable third-party libraries (FR-GR-060)

When a reliable and commonly adopted library is available and suitable, prefer it over custom implementation (security, maintenance, license).

## Current choices
- **Textual** – TUI framework (optional dependency).
- **Tkinter** – GUI (stdlib).
- **JSON** – Task/capture format (stdlib).
- **socket** – Transport (stdlib).

## Decision log
- No custom protocol parsers; use stdlib socket and structured JSON for messages/capture.
- Contract validation: stub in place; full .h/ctypes can use a maintained parser library when added.
