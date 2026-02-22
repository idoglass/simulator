"""Target controller: CRUD with form (Save/Cancel). Uses py-gui."""

import tkinter as tk

from tk_mvc.mvc.base import BaseController
from tk_mvc.mvc.binding import bind_commands
from tk_mvc.components.buttons import primary_button
from tk_mvc.components.form import entry_field, combobox_field
from tk_mvc.components.modals import message_warning, message_error, ask_yes_no


class TargetController(BaseController):
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
        self._status_msg("%d target(s)" % len(items))

    def _form_modal(self, title, initial=None):
        initial = initial or {}
        result = [None]
        win = tk.Toplevel(self.view.frame.winfo_toplevel())
        win.title(title)
        win.transient(self.view.frame.winfo_toplevel())
        win.grab_set()
        f = tk.Frame(win, padx=12, pady=12)
        f.pack(fill=tk.BOTH, expand=True)
        r1, e_id = entry_field(f, "Target ID", initial.get("target_id", "my-target"), width=28)
        r1.pack(fill=tk.X, pady=4)
        r2, e_name = entry_field(f, "Name", initial.get("name", "My Target"), width=28)
        r2.pack(fill=tk.X, pady=4)
        r3, e_host = entry_field(f, "Host", initial.get("host", "127.0.0.1"), width=28)
        r3.pack(fill=tk.X, pady=4)
        r4, e_port = entry_field(f, "Port", str(initial.get("port", 9999)), width=10)
        r4.pack(fill=tk.X, pady=4)
        r5, combo_protocol = combobox_field(f, "Protocol", ["tcp", "udp"], initial.get("protocol", "tcp"), width=10)
        r5.pack(fill=tk.X, pady=4)
        r6, combo_mode = combobox_field(f, "Mode", ["client", "server"], initial.get("mode", "client"), width=10)
        r6.pack(fill=tk.X, pady=4)
        if initial.get("target_id"):
            e_id.config(state=tk.DISABLED)

        def on_save():
            target_id = e_id.get().strip()
            name = e_name.get().strip()
            try:
                port = int(e_port.get().strip())
            except ValueError:
                message_error(win, "Validation", "Port must be 1-65535")
                return
            if not target_id or not name:
                message_error(win, "Validation", "Target ID and Name required")
                return
            if port < 1 or port > 65535:
                message_error(win, "Validation", "Port must be 1-65535")
                return
            result[0] = {
                "target_id": target_id,
                "name": name,
                "host": e_host.get().strip() or "127.0.0.1",
                "port": port,
                "protocol": combo_protocol.get().strip() or "tcp",
                "mode": combo_mode.get().strip() or "client",
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
        r = self._form_modal("Add Target")
        if r:
            self.model.add(r)
            self._status_msg("Target added.")

    def on_edit(self):
        idx = self.view.get_selection_index()
        if idx is None:
            message_warning(self.view.frame.winfo_toplevel(), "Edit", "Select a target first.")
            return
        items = self.model.get_all()
        if idx >= len(items):
            return
        r = self._form_modal("Edit Target", items[idx])
        if r:
            self.model.update(items[idx].get("target_id", ""), r)
            self._status_msg("Target updated.")

    def on_delete(self):
        idx = self.view.get_selection_index()
        if idx is None:
            message_warning(self.view.frame.winfo_toplevel(), "Delete", "Select a target first.")
            return
        if not ask_yes_no(self.view.frame.winfo_toplevel(), "Delete", "Delete this target?"):
            return
        items = self.model.get_all()
        if idx < len(items):
            self.model.delete(items[idx].get("target_id", ""))
        self._status_msg("Target deleted.")
