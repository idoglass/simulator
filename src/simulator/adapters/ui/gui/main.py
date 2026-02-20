"""GUI entry: Tkinter window with run/list/load/compose/create via shared simulation service."""

from __future__ import annotations

import json
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from uuid import uuid4


def run_gui(container: dict[str, object]) -> None:
    """Run GUI mode: window with Run, List, Load task, Compose task, Create task."""
    service = container["simulation_service"]
    root = tk.Tk()
    root.title("Simulator")
    root.geometry("520x320")
    root.minsize(400, 260)

    main = ttk.Frame(root, padding=12)
    main.pack(fill=tk.BOTH, expand=True)

    ttk.Label(main, text="Simulator (Run / List / Load / Compose / Create tasks)", font=("", 10)).pack(anchor=tk.W)

    output = tk.Text(main, height=10, width=60, wrap=tk.WORD, state=tk.DISABLED)
    output.pack(fill=tk.BOTH, expand=True, pady=(8, 8))

    def _out(msg: str) -> None:
        output.config(state=tk.NORMAL)
        output.delete("1.0", tk.END)
        output.insert(tk.END, msg)
        output.config(state=tk.DISABLED)

    def run_simulation() -> None:
        _out("Running...\n")
        root.update_idletasks()
        try:
            result = service.run(
                run_id=f"run-{uuid4().hex[:8]}",
                target_id="default-target",
                task_id="ping-smoke",
                protocol="tcp",
            )
            v = result.get("verification") or {}
            _out(f"Run {result.get('run_id', '')}: {v.get('summary', '')} (passed={v.get('passed')})\n")
        except Exception as e:
            _out(f"Error: {e!s}\n")

    def list_tasks() -> None:
        try:
            tasks = service.list_tasks()
            lines = [f"- {t.get('task_id', '')}: {t.get('name', '')}" for t in tasks]
            _out("Tasks:\n" + ("\n".join(lines) if lines else "(none)"))
        except Exception as e:
            _out(f"Error: {e!s}")

    def load_task() -> None:
        path = filedialog.askopenfilename(title="Select .task.json", filetypes=[("JSON", "*.task.json *.json"), ("All", "*")])
        if not path:
            return
        try:
            r = service.load_task(path)
            if r.get("ok"):
                _out(f"Loaded task: {r.get('task_id', '')}\n")
            else:
                _out(f"Load failed: {r.get('error_code', '')} {r.get('message', '')}\n")
        except Exception as e:
            _out(f"Error: {e!s}\n")

    def compose_task() -> None:
        tasks = service.list_tasks()
        ids = [t.get("task_id", "") for t in tasks if t.get("task_id")]
        if len(ids) < 2:
            _out("Need at least 2 registered tasks to compose. List tasks first.\n")
            return
        try:
            r = service.compose_task(ids[:2], {"task_id": "composed-1", "name": "Composed"})
            if r.get("ok"):
                _out(f"Composed task: {r.get('task_id', '')}\n")
            else:
                _out(f"Compose failed: {r.get('error_code', '')}\n")
        except Exception as e:
            _out(f"Error: {e!s}\n")

    def create_task() -> None:
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

        def do_create() -> None:
            try:
                steps = json.loads(e_steps.get("1.0", tk.END))
                defn = {"task_id": e_id.get().strip(), "name": e_name.get().strip(), "steps": steps, "payloads": {}, "defaults": {}}
                r = service.create_task(defn)
                if r.get("ok"):
                    messagebox.showinfo("Create task", f"Created: {r.get('task_id', '')}")
                    win.destroy()
                else:
                    messagebox.showerror("Create task", r.get("error_code", "") + " " + str(r.get("message", "")))
            except json.JSONDecodeError as e:
                messagebox.showerror("Create task", f"Invalid JSON: {e!s}")
        ttk.Button(f, text="Create", command=do_create).pack(pady=8)

    btn_frame = ttk.Frame(main)
    btn_frame.pack(fill=tk.X)
    ttk.Button(btn_frame, text="Run", command=run_simulation).pack(side=tk.LEFT, padx=(0, 4))
    ttk.Button(btn_frame, text="List tasks", command=list_tasks).pack(side=tk.LEFT, padx=(0, 4))
    ttk.Button(btn_frame, text="Load task", command=load_task).pack(side=tk.LEFT, padx=(0, 4))
    ttk.Button(btn_frame, text="Compose", command=compose_task).pack(side=tk.LEFT, padx=(0, 4))
    ttk.Button(btn_frame, text="Create task", command=create_task).pack(side=tk.LEFT)

    _out("Ready. Run / List / Load / Compose / Create tasks.")
    root.mainloop()
