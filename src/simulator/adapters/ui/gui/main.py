"""GUI entry: py-gui App with notebook (Targets, Tasks, Contracts, Run) and footer (target selector + Ping)."""

from __future__ import annotations

import json
import sys
import threading
import tkinter as tk
from pathlib import Path
from tkinter import ttk, filedialog
from uuid import uuid4

# Ensure py-gui is importable (repo root = parents[5] from .../simulator/src/simulator/adapters/ui/gui/main.py)
_repo_root = Path(__file__).resolve().parents[5]
_py_gui_src = _repo_root / "py-gui" / "src"
if _py_gui_src.is_dir() and str(_py_gui_src) not in sys.path:
    sys.path.insert(0, str(_py_gui_src))

from tk_mvc.app import App
from tk_mvc.components.notebook import notebook, add_tab
from tk_mvc.components.status_bar import status_bar
from tk_mvc.components.modals import message_info, message_error

from simulator.adapters.ui.gui.models import TargetModel, TaskModel, ContractModel
from simulator.adapters.ui.gui.views import TargetView, TaskView, ContractView
from simulator.adapters.ui.gui.controllers import TargetController, TaskController, ContractController


def run_gui(container: dict) -> None:
    """Run GUI: py-gui App with notebook (Targets, Tasks, Contracts, Run) and footer (target ref + Ping)."""
    service = container["simulation_service"]
    list_targets = container["list_targets"]
    ping_target = container["ping_target"]

    def main_view_factory(root: tk.Tk):
        main_container = tk.Frame(root, padx=0, pady=0)
        status = status_bar(main_container, initial_text="Ready")
        status.pack(side=tk.BOTTOM, fill=tk.X)
        footer = ttk.Frame(main_container, padding=8)
        footer.pack(side=tk.BOTTOM, fill=tk.X)
        ttk.Label(footer, text="Target:").pack(side=tk.LEFT, padx=(0, 4))
        footer_combo = ttk.Combobox(footer, width=24, state="readonly")
        footer_combo.pack(side=tk.LEFT, padx=(0, 8))
        ping_btn = ttk.Button(footer, text="Ping")
        ping_btn.pack(side=tk.LEFT, padx=(0, 8))
        footer_status = ttk.Label(footer, text="Ping: —")
        footer_status.pack(side=tk.LEFT)

        def refresh_footer_combo():
            targets = list_targets()
            ids = [t.target_id for t in targets]
            footer_combo["values"] = ids
            if ids and footer_combo.get() not in ids:
                footer_combo.set(ids[0] if ids else "")

        def do_ping():
            tid = footer_combo.get().strip()
            if not tid:
                footer_status.config(text="Ping: Select a target")
                return
            ping_btn.config(state=tk.DISABLED)
            footer_status.config(text="Ping: ...")

            def run():
                result = ping_target(tid)
                def update():
                    ping_btn.config(state=tk.NORMAL)
                    if result.get("ok"):
                        footer_status.config(text="Ping: OK")
                    else:
                        footer_status.config(text="Ping: %s" % result.get("error", "unreachable"))
                root.after(0, update)
            threading.Thread(target=run, daemon=True).start()

        ping_btn.config(command=do_ping)
        refresh_footer_combo()

        nb = notebook(main_container)
        nb.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)

        # Tab: Targets
        target_tab = tk.Frame(nb, padx=4, pady=4)
        target_model = TargetModel(container)
        target_model.add_listener(refresh_footer_combo)
        target_view = TargetView(target_tab)
        target_controller = TargetController(target_model, target_view, status_bar=status)
        target_view.controller = target_controller
        target_view.frame.pack(fill=tk.BOTH, expand=True)
        target_controller._refresh_list()
        add_tab(nb, target_tab, "Targets")

        # Tab: Tasks
        task_tab = tk.Frame(nb, padx=4, pady=4)
        task_model = TaskModel(container)
        task_view = TaskView(task_tab)
        task_controller = TaskController(task_model, task_view, status_bar=status)
        task_view.controller = task_controller
        task_view.frame.pack(fill=tk.BOTH, expand=True)
        task_controller._refresh_list()
        add_tab(nb, task_tab, "Tasks")

        # Tab: Contracts
        contract_tab = tk.Frame(nb, padx=4, pady=4)
        contract_model = ContractModel(container)
        contract_view = ContractView(contract_tab)
        contract_controller = ContractController(contract_model, contract_view, status_bar=status)
        contract_view.controller = contract_controller
        contract_view.frame.pack(fill=tk.BOTH, expand=True)
        contract_controller._refresh_list()
        add_tab(nb, contract_tab, "Contracts")

        # Tab: Run
        run_tab = tk.Frame(nb, padx=8, pady=8)
        ttk.Label(run_tab, text="Simulator (Run / List / Load / Compose / Create tasks)", font=("", 10)).pack(anchor=tk.W)
        output = tk.Text(run_tab, height=10, width=60, wrap=tk.WORD, state=tk.DISABLED)
        output.pack(fill=tk.BOTH, expand=True, pady=(8, 8))

        def out(msg: str):
            output.config(state=tk.NORMAL)
            output.delete("1.0", tk.END)
            output.insert(tk.END, msg)
            output.config(state=tk.DISABLED)

        def get_selected_target_id():
            tid = footer_combo.get().strip()
            if tid:
                return tid
            targets = list_targets()
            return targets[0].target_id if targets else None

        def run_simulation():
            tid = get_selected_target_id()
            if not tid:
                out("No target selected. Select a target in the footer.\n")
                return
            out("Running...\n")
            root.update_idletasks()
            try:
                result = service.run(
                    run_id="run-%s" % uuid4().hex[:8],
                    target_id=tid,
                    task_id="ping-smoke",
                    protocol="tcp",
                )
                v = result.get("verification") or {}
                out("Run %s: %s (passed=%s)\n" % (result.get("run_id", ""), v.get("summary", ""), v.get("passed")))
            except Exception as e:
                out("Error: %s\n" % e)

        def list_tasks():
            try:
                tasks = service.list_tasks()
                lines = ["- %s: %s" % (t.get("task_id", ""), t.get("name", "")) for t in tasks]
                out("Tasks:\n" + ("\n".join(lines) if lines else "(none)"))
            except Exception as e:
                out("Error: %s" % e)

        def load_task():
            path = filedialog.askopenfilename(
                title="Select .task.json",
                filetypes=[("JSON", "*.task.json *.json"), ("All", "*")],
            )
            if not path:
                return
            try:
                r = service.load_task(path)
                if r.get("ok"):
                    out("Loaded task: %s\n" % r.get("task_id", ""))
                else:
                    out("Load failed: %s %s\n" % (r.get("error_code", ""), r.get("message", "")))
            except Exception as e:
                out("Error: %s\n" % e)

        def compose_task():
            tasks = service.list_tasks()
            ids = [t.get("task_id", "") for t in tasks if t.get("task_id")]
            if len(ids) < 2:
                out("Need at least 2 registered tasks to compose. List tasks first.\n")
                return
            try:
                r = service.compose_task(ids[:2], {"task_id": "composed-1", "name": "Composed"})
                if r.get("ok"):
                    out("Composed task: %s\n" % r.get("task_id", ""))
                else:
                    out("Compose failed: %s\n" % r.get("error_code", ""))
            except Exception as e:
                out("Error: %s\n" % e)

        def create_task():
            win = tk.Toplevel(root)
            win.title("Create task")
            win.geometry("400x280")
            f = ttk.Frame(win, padding=8)
            f.pack(fill=tk.BOTH, expand=True)
            ttk.Label(f, text="Task ID:").pack(anchor=tk.W)
            e_id = ttk.Entry(f, width=40)
            e_id.pack(fill=tk.X, pady=(0, 6))
            e_id.insert(0, "my-task")
            ttk.Label(f, text="Name:").pack(anchor=tk.W)
            e_name = ttk.Entry(f, width=40)
            e_name.pack(fill=tk.X, pady=(0, 6))
            e_name.insert(0, "My Task")
            ttk.Label(f, text="Steps (JSON array, e.g. []):").pack(anchor=tk.W)
            e_steps = tk.Text(f, height=4, width=50)
            e_steps.pack(fill=tk.X, pady=(0, 6))
            e_steps.insert("1.0", "[]")

            def do_create():
                try:
                    steps = json.loads(e_steps.get("1.0", tk.END))
                    defn = {
                        "task_id": e_id.get().strip(),
                        "name": e_name.get().strip(),
                        "steps": steps,
                        "payloads": {},
                        "defaults": {},
                    }
                    r = service.create_task(defn)
                    if r.get("ok"):
                        message_info(win, "Create task", "Created: %s" % r.get("task_id", ""))
                        win.destroy()
                    else:
                        message_error(win, "Create task", r.get("error_code", "") + " " + str(r.get("message", "")))
                except json.JSONDecodeError as e:
                    message_error(win, "Create task", "Invalid JSON: %s" % e)
            ttk.Button(f, text="Create", command=do_create).pack(pady=8)

        btn_frame = ttk.Frame(run_tab)
        btn_frame.pack(fill=tk.X)
        ttk.Button(btn_frame, text="Run", command=run_simulation).pack(side=tk.LEFT, padx=(0, 4))
        ttk.Button(btn_frame, text="List tasks", command=list_tasks).pack(side=tk.LEFT, padx=(0, 4))
        ttk.Button(btn_frame, text="Load task", command=load_task).pack(side=tk.LEFT, padx=(0, 4))
        ttk.Button(btn_frame, text="Compose", command=compose_task).pack(side=tk.LEFT, padx=(0, 4))
        ttk.Button(btn_frame, text="Create task", command=create_task).pack(side=tk.LEFT)

        add_tab(nb, run_tab, "Run")
        out("Ready. Run uses target from footer. List / Load / Compose / Create tasks.")

        class MainView:
            frame = main_container
        return MainView()

    app = App(
        title="Simulator",
        geometry="620x520",
        main_view_factory=main_view_factory,
        menu_factory=None,
    )
    app.setup()
    app.run()
