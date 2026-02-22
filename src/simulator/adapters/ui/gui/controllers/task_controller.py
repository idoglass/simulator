"""Task controller: CRUD with Load/Compose/Create, step editor, payload_ref combobox. Uses py-gui."""

import tkinter as tk
from tkinter import ttk, filedialog

from tk_mvc.mvc.base import BaseController
from tk_mvc.mvc.binding import bind_commands
from tk_mvc.components.buttons import primary_button, secondary_button
from tk_mvc.components.form import entry_field, combobox_field
from tk_mvc.components.modals import message_warning, message_error, message_info, ask_yes_no


class TaskController(BaseController):
    def __init__(self, model, view, status_bar=None):
        super().__init__(model, view)
        self._status = status_bar
        self.view.build()
        bind_commands(self.view, self, {"btn_add": "on_add", "btn_edit": "on_edit", "btn_delete": "on_delete"})
        self.model.add_listener(self._refresh_list)

    def _status_msg(self, msg):
        if self._status and hasattr(self._status, "set_text"):
            self._status.set_text(msg)

    def _refresh_list(self):
        items = self.model.get_all()
        self.view.set_items(items)
        self._status_msg("%d task(s)" % len(items))

    def _step_label(self, step):
        sid = step.get("step_id", "?")
        action = step.get("action", "send")
        msg = step.get("message_type", "")
        expect = step.get("expect") or {}
        matcher = expect.get("matcher") or {}
        exp_msg = matcher.get("message_type", "")
        if exp_msg:
            return "%s: %s %s -> expect %s" % (sid, action, msg, exp_msg)
        return "%s: %s %s" % (sid, action, msg)

    def _step_modal(self, parent_win, initial=None, payload_keys=None):
        """Add/Edit one step. payload_keys = list for payload_ref combobox (ref field)."""
        initial = initial or {}
        payload_keys = payload_keys or []
        expect = initial.get("expect") or {}
        matcher = expect.get("matcher") or {}
        result = [None]
        win = tk.Toplevel(parent_win)
        win.title("Edit Step" if initial.get("step_id") else "Add Step")
        win.transient(parent_win)
        win.grab_set()
        f = tk.Frame(win, padx=12, pady=12)
        f.pack(fill=tk.BOTH, expand=True)
        r1, e_step_id = entry_field(f, "Step ID", initial.get("step_id", "s1"), width=16)
        r1.pack(fill=tk.X, pady=4)
        r2, combo_action = combobox_field(f, "Action", ["send", "receive_expectation"], initial.get("action", "send"), width=18)
        r2.pack(fill=tk.X, pady=4)
        r3, e_message_type = entry_field(f, "Message type", initial.get("message_type", ""), width=24)
        r3.pack(fill=tk.X, pady=4)
        combo_payload = None
        e_payload_ref = None
        if payload_keys:
            r4, combo_payload = combobox_field(f, "Payload ref", [""] + list(payload_keys), initial.get("payload_ref") or "", width=16)
        else:
            r4, e_payload_ref = entry_field(f, "Payload ref (optional)", initial.get("payload_ref", "") or "", width=16)
        r4.pack(fill=tk.X, pady=4)
        r5, combo_exp_dir = combobox_field(f, "Expect direction", ["receive"], matcher.get("direction", "receive"), width=10)
        r5.pack(fill=tk.X, pady=2)
        r6, e_exp_msg = entry_field(f, "Expect message type", matcher.get("message_type", ""), width=24)
        r6.pack(fill=tk.X, pady=2)
        r7, e_exp_count = entry_field(f, "Expected count", str(expect.get("expected_count", 1)), width=8)
        r7.pack(fill=tk.X, pady=2)
        r8, combo_comparison = combobox_field(f, "Comparison", ["eq"], expect.get("comparison", "eq"), width=8)
        r8.pack(fill=tk.X, pady=2)
        r9, e_timeout = entry_field(f, "Timeout (ms)", str(initial.get("timeout_ms", 1000)), width=10)
        r9.pack(fill=tk.X, pady=4)

        def on_ok():
            step_id = e_step_id.get().strip()
            message_type = e_message_type.get().strip()
            if not step_id:
                message_error(win, "Validation", "Step ID required")
                return
            if not message_type:
                message_error(win, "Validation", "Message type required")
                return
            try:
                timeout_ms = int(e_timeout.get().strip() or "1000")
            except ValueError:
                message_error(win, "Validation", "Timeout must be a number")
                return
            exp_count_val = 1
            try:
                exp_count_val = int(e_exp_count.get().strip() or "1")
            except ValueError:
                pass
            payload_ref = (combo_payload.get().strip() if combo_payload else (e_payload_ref.get().strip() if e_payload_ref else "")) or None
            exp_msg = e_exp_msg.get().strip()
            expect_block = None
            if exp_msg:
                expect_block = {
                    "matcher": {"direction": combo_exp_dir.get().strip() or "receive", "message_type": exp_msg},
                    "expected_count": exp_count_val,
                    "comparison": combo_comparison.get().strip() or "eq",
                }
            result[0] = {
                "step_id": step_id,
                "action": combo_action.get().strip() or "send",
                "message_type": message_type,
                "payload_ref": payload_ref,
                "expect": expect_block,
                "timeout_ms": timeout_ms,
            }
            win.destroy()

        def on_cancel():
            win.destroy()

        btn_f = tk.Frame(f)
        btn_f.pack(fill=tk.X, pady=(12, 0))
        primary_button(btn_f, "OK", on_ok).pack(side=tk.LEFT, padx=(0, 6))
        tk.Button(btn_f, text="Cancel", command=on_cancel, width=8).pack(side=tk.LEFT)
        parent = self.view.frame.winfo_toplevel()
        win.geometry("+%d+%d" % (parent.winfo_rootx() + 80, parent.winfo_rooty() + 80))
        win.wait_window(win)
        return result[0]

    def _task_form_modal(self, title, initial=None):
        """Full task form: task_id, name, steps list (Add/Edit/Remove step). Step editor uses payload_ref combobox from payloads keys."""
        initial = initial or {}
        steps_list = list(initial.get("steps") or [])
        payloads = dict(initial.get("payloads") or {})
        payload_keys = list(payloads.keys())
        result = [None]
        win = tk.Toplevel(self.view.frame.winfo_toplevel())
        win.title(title)
        win.transient(self.view.frame.winfo_toplevel())
        win.grab_set()
        f = tk.Frame(win, padx=12, pady=12)
        f.pack(fill=tk.BOTH, expand=True)
        r1, e_id = entry_field(f, "Task ID", initial.get("task_id", "my-task"), width=28)
        r1.pack(fill=tk.X, pady=4)
        r2, e_name = entry_field(f, "Name", initial.get("name", "My Task"), width=28)
        r2.pack(fill=tk.X, pady=4)
        if initial.get("task_id"):
            e_id.config(state=tk.DISABLED)
        tk.Label(f, text="Steps:").pack(anchor=tk.W)
        steps_frame = tk.Frame(f)
        steps_frame.pack(fill=tk.BOTH, expand=True, pady=4)
        scrollbar = tk.Scrollbar(steps_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        steps_lb = tk.Listbox(steps_frame, height=5, width=50, yscrollcommand=scrollbar.set)
        steps_lb.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=steps_lb.yview)
        step_btn_f = tk.Frame(f)
        step_btn_f.pack(fill=tk.X, pady=2)

        def refresh_steps_listbox():
            steps_lb.delete(0, tk.END)
            for s in steps_list:
                steps_lb.insert(tk.END, self._step_label(s))

        def on_add_step():
            new_step = self._step_modal(win, payload_keys=payload_keys)
            if new_step:
                steps_list.append(new_step)
                refresh_steps_listbox()

        def on_edit_step():
            sel = steps_lb.curselection()
            if not sel:
                message_warning(win, "Edit Step", "Select a step first.")
                return
            idx = int(sel[0])
            if 0 <= idx < len(steps_list):
                edited = self._step_modal(win, initial=steps_list[idx], payload_keys=payload_keys)
                if edited:
                    steps_list[idx] = edited
                    refresh_steps_listbox()

        def on_remove_step():
            sel = steps_lb.curselection()
            if not sel:
                message_warning(win, "Remove Step", "Select a step first.")
                return
            idx = int(sel[0])
            if 0 <= idx < len(steps_list):
                steps_list.pop(idx)
                refresh_steps_listbox()

        secondary_button(step_btn_f, "Add step", on_add_step).pack(side=tk.LEFT, padx=(0, 6))
        tk.Button(step_btn_f, text="Edit step", command=on_edit_step).pack(side=tk.LEFT, padx=(0, 6))
        tk.Button(step_btn_f, text="Remove step", command=on_remove_step).pack(side=tk.LEFT)
        refresh_steps_listbox()

        def on_save():
            task_id = e_id.get().strip()
            name = e_name.get().strip()
            if not task_id or not name:
                message_error(win, "Validation", "Task ID and Name required")
                return
            result[0] = {
                "task_id": task_id,
                "name": name,
                "steps": list(steps_list),
                "payloads": initial.get("payloads") or {},
                "defaults": initial.get("defaults") or {},
            }
            win.destroy()

        def on_cancel():
            win.destroy()

        btn_f = tk.Frame(f)
        btn_f.pack(fill=tk.X, pady=(12, 0))
        primary_button(btn_f, "Save", on_save).pack(side=tk.LEFT, padx=(0, 6))
        tk.Button(btn_f, text="Cancel", command=on_cancel, width=8).pack(side=tk.LEFT)
        parent = self.view.frame.winfo_toplevel()
        win.geometry("+%d+%d" % (parent.winfo_rootx() + 50, parent.winfo_rooty() + 50))
        win.wait_window(win)
        return result[0]

    def on_add(self):
        win = tk.Toplevel(self.view.frame.winfo_toplevel())
        win.title("Add Task")
        win.transient(self.view.frame.winfo_toplevel())
        win.grab_set()
        f = tk.Frame(win, padx=12, pady=12)
        f.pack(fill=tk.BOTH, expand=True)
        ttk.Label(f, text="Add task by:").pack(anchor=tk.W)

        def load_from_file():
            win.destroy()
            path = filedialog.askopenfilename(parent=self.view.frame.winfo_toplevel(), title="Select .task.json",
                                             filetypes=[("JSON", "*.task.json *.json"), ("All", "*")])
            if path:
                r = self.model.load_task(path)
                if r.get("ok"):
                    self._status_msg("Loaded: %s" % r.get("task_id", ""))
                    message_info(self.view.frame.winfo_toplevel(), "Load Task", "Loaded: %s" % r.get("task_id", ""))
                else:
                    message_error(self.view.frame.winfo_toplevel(), "Load Task", r.get("error_code", "") + " " + str(r.get("message", "")))

        def compose():
            win.destroy()
            tasks = self.model.get_all()
            if len(tasks) < 2:
                message_warning(self.view.frame.winfo_toplevel(), "Compose", "Need at least 2 tasks. Load or create tasks first.")
                return
            task_ids = [t.get("task_id", "") for t in tasks if t.get("task_id")]
            result = [None]
            cwin = tk.Toplevel(self.view.frame.winfo_toplevel())
            cwin.title("Compose Task")
            cwin.transient(self.view.frame.winfo_toplevel())
            cwin.grab_set()
            cf = tk.Frame(cwin, padx=12, pady=12)
            cf.pack(fill=tk.BOTH, expand=True)
            ttk.Label(cf, text="Base tasks (ref): select two or more").pack(anchor=tk.W)
            lb = tk.Listbox(cf, selectmode=tk.MULTIPLE, height=6, width=40)
            for tid in task_ids:
                lb.insert(tk.END, tid)
            lb.pack(fill=tk.X, pady=4)
            r1, e_id = entry_field(cf, "New task ID", "composed-1", width=24)
            r1.pack(fill=tk.X, pady=4)
            r2, e_name = entry_field(cf, "Name", "Composed", width=24)
            r2.pack(fill=tk.X, pady=4)

            def do_compose():
                sel = lb.curselection()
                if len(sel) < 2:
                    message_error(cwin, "Compose", "Select at least 2 base tasks")
                    return
                base_ids = [task_ids[i] for i in sel]
                overrides = {"task_id": e_id.get().strip() or "composed-1", "name": e_name.get().strip() or "Composed"}
                r = self.model.compose_task(base_ids, overrides)
                cwin.destroy()
                if r.get("ok"):
                    self._status_msg("Composed: %s" % r.get("task_id", ""))
                    message_info(self.view.frame.winfo_toplevel(), "Compose", "Created: %s" % r.get("task_id", ""))
                else:
                    message_error(self.view.frame.winfo_toplevel(), "Compose", r.get("error_code", "") + " " + str(r.get("message", "")))

            tk.Frame(cf).pack(fill=tk.X, pady=(8, 0))
            primary_button(cf, "Compose", do_compose).pack(side=tk.LEFT, padx=(0, 6))
            tk.Button(cf, text="Cancel", command=cwin.destroy, width=8).pack(side=tk.LEFT)

        def create_from_scratch():
            win.destroy()
            r = self._task_form_modal("Create Task")
            if r:
                res = self.model.add(r)
                if res.get("ok"):
                    self._status_msg("Task created.")
                    message_info(self.view.frame.winfo_toplevel(), "Create Task", "Created: %s" % res.get("task_id", ""))
                else:
                    message_error(self.view.frame.winfo_toplevel(), "Create Task", res.get("error_code", "") + " " + str(res.get("message", "")))

        tk.Button(f, text="Load from file", command=load_from_file).pack(fill=tk.X, pady=4)
        tk.Button(f, text="Compose from existing tasks", command=compose).pack(fill=tk.X, pady=4)
        tk.Button(f, text="Create from scratch", command=create_from_scratch).pack(fill=tk.X, pady=4)
        parent = self.view.frame.winfo_toplevel()
        win.geometry("+%d+%d" % (parent.winfo_rootx() + 80, parent.winfo_rooty() + 80))

    def on_edit(self):
        idx = self.view.get_selection_index()
        if idx is None:
            message_warning(self.view.frame.winfo_toplevel(), "Edit", "Select a task first.")
            return
        items = self.model.get_all()
        if idx >= len(items):
            return
        task_id = items[idx].get("task_id", "")
        full = self.model.get(task_id)
        if not full:
            message_error(self.view.frame.winfo_toplevel(), "Edit", "Task not found")
            return
        r = self._task_form_modal("Edit Task", full)
        if r:
            self.model.delete(task_id)
            res = self.model.add(r)
            if res.get("ok"):
                self._status_msg("Task updated.")
            else:
                message_error(self.view.frame.winfo_toplevel(), "Edit Task", res.get("error_code", ""))

    def on_delete(self):
        idx = self.view.get_selection_index()
        if idx is None:
            message_warning(self.view.frame.winfo_toplevel(), "Delete", "Select a task first.")
            return
        if not ask_yes_no(self.view.frame.winfo_toplevel(), "Delete", "Delete this task?"):
            return
        items = self.model.get_all()
        if idx >= len(items):
            return
        tid = items[idx].get("task_id", "")
        if tid:
            r = self.model.delete(tid)
            if r.get("ok"):
                self._status_msg("Task deleted.")
            else:
                message_error(self.view.frame.winfo_toplevel(), "Delete", r.get("error_code", ""))
