"""Contract view: listbox and Add/Edit/Delete buttons (py-gui BaseView)."""

import tkinter as tk

from tk_mvc.mvc.base import BaseView
from tk_mvc.components.buttons import primary_button, secondary_button, danger_button


class ContractView(BaseView):
    def build(self):
        self.frame = tk.Frame(self.parent, padx=10, pady=10)
        list_frame = tk.Frame(self.frame)
        list_frame.pack(fill=tk.BOTH, expand=True)
        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.listbox = tk.Listbox(list_frame, yscrollcommand=scrollbar.set, height=10)
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.listbox.yview)
        btn_frame = tk.Frame(self.frame)
        btn_frame.pack(fill=tk.X, pady=(8, 0))
        self.btn_add = primary_button(btn_frame, "Add", None)
        self.btn_add.pack(side=tk.LEFT, padx=(0, 6))
        self.btn_edit = secondary_button(btn_frame, "Edit", None)
        self.btn_edit.pack(side=tk.LEFT, padx=(0, 6))
        self.btn_delete = danger_button(btn_frame, "Delete", None)
        self.btn_delete.pack(side=tk.LEFT)
        return self.frame

    def set_items(self, items):
        self.listbox.delete(0, tk.END)
        for item in items:
            row = item.get("contract_id", "") + "  " + item.get("source_path", "")
            self.listbox.insert(tk.END, row)

    def get_selection_index(self):
        sel = self.listbox.curselection()
        return int(sel[0]) if sel else None

    def get_selection(self):
        sel = self.listbox.curselection()
        if not sel:
            return None
        return self.listbox.get(sel[0])
