"""Contract controller: CRUD with form (Save/Cancel), folder selector for source path. Uses py-gui."""

import tkinter as tk
from tkinter import filedialog

from tk_mvc.mvc.base import BaseController
from tk_mvc.mvc.binding import bind_commands
from tk_mvc.components.buttons import primary_button
from tk_mvc.components.form import entry_field, combobox_field
from tk_mvc.components.modals import message_warning, message_error, ask_yes_no


class ContractController(BaseController):
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
        self._status_msg("%d contract(s)" % len(items))

    def _form_modal(self, title, initial=None):
        initial = initial or {}
        result = [None]
        win = tk.Toplevel(self.view.frame.winfo_toplevel())
        win.title(title)
        win.transient(self.view.frame.winfo_toplevel())
        win.grab_set()
        f = tk.Frame(win, padx=12, pady=12)
        f.pack(fill=tk.BOTH, expand=True)
        r1, e_id = entry_field(f, "Contract ID", initial.get("contract_id", "my-contract"), width=28)
        r1.pack(fill=tk.X, pady=4)
        r2, e_app = entry_field(f, "Application ref", initial.get("application_ref", "default"), width=28)
        r2.pack(fill=tk.X, pady=4)
        r3, combo_st = combobox_field(f, "Source type", ["repo_h", "user_h"], initial.get("source_type", "user_h"), width=10)
        r3.pack(fill=tk.X, pady=4)
        tk.Label(f, text="Source path:").pack(anchor=tk.W)
        path_row = tk.Frame(f)
        path_row.pack(fill=tk.X, pady=2)
        e_path = tk.Entry(path_row, width=36)
        e_path.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 4))
        e_path.insert(0, initial.get("source_path", ""))

        def choose_folder():
            path = filedialog.askdirectory(parent=win, title="Select folder")
            if path:
                e_path.delete(0, tk.END)
                e_path.insert(0, path)

        tk.Button(path_row, text="Browse...", command=choose_folder).pack(side=tk.LEFT)
        r5, e_ver = entry_field(f, "Version", initial.get("version", "0.1.0"), width=12)
        r5.pack(fill=tk.X, pady=4)
        r6, e_checksum = entry_field(f, "Checksum (optional)", initial.get("checksum_sha256", ""), width=36)
        r6.pack(fill=tk.X, pady=4)
        if initial.get("contract_id"):
            e_id.config(state=tk.DISABLED)

        def on_save():
            if not e_id.get().strip():
                message_error(win, "Validation", "Contract ID required")
                return
            if not e_path.get().strip():
                message_error(win, "Validation", "Source path required")
                return
            result[0] = {
                "contract_id": e_id.get().strip(),
                "application_ref": e_app.get().strip() or "default",
                "source_type": combo_st.get().strip() or "user_h",
                "source_path": e_path.get().strip(),
                "version": e_ver.get().strip() or "0.1.0",
                "checksum_sha256": e_checksum.get().strip(),
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
        r = self._form_modal("Add Contract")
        if r:
            self.model.add(r)
            self._status_msg("Contract added.")

    def on_edit(self):
        idx = self.view.get_selection_index()
        if idx is None:
            message_warning(self.view.frame.winfo_toplevel(), "Edit", "Select a contract first.")
            return
        items = self.model.get_all()
        if idx >= len(items):
            return
        r = self._form_modal("Edit Contract", items[idx])
        if r:
            self.model.update(items[idx].get("contract_id", ""), r)
            self._status_msg("Contract updated.")

    def on_delete(self):
        idx = self.view.get_selection_index()
        if idx is None:
            message_warning(self.view.frame.winfo_toplevel(), "Delete", "Select a contract first.")
            return
        if not ask_yes_no(self.view.frame.winfo_toplevel(), "Delete", "Delete this contract?"):
            return
        items = self.model.get_all()
        if idx < len(items):
            self.model.delete(items[idx].get("contract_id", ""))
        self._status_msg("Contract deleted.")
