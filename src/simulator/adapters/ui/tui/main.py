"""TUI entry: Textual app with run/list/load/compose/create via shared simulation service."""

from __future__ import annotations

from uuid import uuid4

from textual.app import App, ComposeResult
from textual.containers import Container
from textual.widgets import Button, Footer, Header, Static


def run_tui(container: dict[str, object]) -> None:
    """Run TUI mode (Textual). Uses shared simulation service."""
    service = container["simulation_service"]
    app = SimulatorTuiApp(service=service)
    app.run()


class SimulatorTuiApp(App[None]):
    """TUI: Run, List, Load, Compose, Create tasks via shared engine."""

    BINDINGS = [
        ("r", "run", "Run"),
        ("l", "list_tasks", "List tasks"),
        ("o", "load_task", "Load task"),
        ("c", "compose_task", "Compose"),
        ("n", "create_task", "Create task"),
        ("q", "quit", "Quit"),
    ]

    def __init__(self, service: object) -> None:
        super().__init__()
        self._service = service

    def compose(self) -> ComposeResult:
        yield Header(show_clock=False)
        yield Container(
            Static("Simulator TUI: r=Run l=List o=Load c=Compose n=Create q=Quit", id="title"),
            Button("Run", id="run"),
            Button("List tasks", id="list"),
            Button("Load task", id="load"),
            Button("Compose", id="compose"),
            Button("Create task", id="create"),
            Static("", id="output"),
        )
        yield Footer()

    def on_mount(self) -> None:
        self.query_one("#output", Static).update("Ready. [r] Run [l] List [o] Load [c] Compose [n] Create task.")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        bid = event.button.id
        if bid == "run":
            self._do_run()
        elif bid == "list":
            self._do_list()
        elif bid == "load":
            self._do_load("")
        elif bid == "compose":
            self._do_compose()
        elif bid == "create":
            self._do_create()

    def action_run(self) -> None:
        self._do_run()

    def action_list_tasks(self) -> None:
        self._do_list()

    def action_load_task(self) -> None:
        self._do_load("")

    def action_compose_task(self) -> None:
        self._do_compose()

    def action_create_task(self) -> None:
        self._do_create()

    def _do_run(self) -> None:
        out = self.query_one("#output", Static)
        out.update("Running...")
        try:
            result = self._service.run(
                run_id=f"run-{uuid4().hex[:8]}",
                target_id="default-target",
                task_id="ping-smoke",
                protocol="tcp",
            )
            v = result.get("verification") or {}
            out.update(f"Run {result.get('run_id', '')}: {v.get('summary', '')} (passed={v.get('passed')})")
        except Exception as e:
            out.update(f"Error: {e!s}")

    def _do_list(self) -> None:
        out = self.query_one("#output", Static)
        try:
            tasks = self._service.list_tasks()
            lines = [f"- {t.get('task_id', '')}: {t.get('name', '')}" for t in tasks]
            out.update("Tasks:\n" + ("\n".join(lines) if lines else "(none)"))
        except Exception as e:
            out.update(f"Error: {e!s}")

    def _do_load(self, path: str) -> None:
        out = self.query_one("#output", Static)
        if not path:
            out.update("Load task: provide path to .task.json (e.g. tests/fixtures/tasks/ping-smoke.task.json)")
            return
        try:
            r = self._service.load_task(path)
            if r.get("ok"):
                out.update(f"Loaded task: {r.get('task_id', '')}")
            else:
                out.update(f"Load failed: {r.get('error_code', '')}")
        except Exception as e:
            out.update(f"Error: {e!s}")

    def _do_compose(self) -> None:
        out = self.query_one("#output", Static)
        try:
            tasks = self._service.list_tasks()
            ids = [t.get("task_id", "") for t in tasks if t.get("task_id")]
            if len(ids) < 2:
                out.update("Need at least 2 tasks to compose. List tasks first.")
                return
            r = self._service.compose_task(ids[:2], {"task_id": "composed-1", "name": "Composed"})
            if r.get("ok"):
                out.update(f"Composed task: {r.get('task_id', '')}")
            else:
                out.update(f"Compose failed: {r.get('error_code', '')}")
        except Exception as e:
            out.update(f"Error: {e!s}")

    def _do_create(self) -> None:
        out = self.query_one("#output", Static)
        try:
            defn = {"task_id": "tui-created-1", "name": "TUI created", "steps": [], "payloads": {}, "defaults": {}}
            r = self._service.create_task(defn)
            if r.get("ok"):
                out.update(f"Created task: {r.get('task_id', '')}")
            else:
                out.update(f"Create failed: {r.get('error_code', '')}")
        except Exception as e:
            out.update(f"Error: {e!s}")
