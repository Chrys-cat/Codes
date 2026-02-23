import tkinter as tk
from tkinter import ttk, messagebox

from config import PROGRAM_FILE, PROGRAM_FIELDS, COLLEGE_FILE, STUDENT_FILE
from utils import load_data, save_data


class ProgramTab:

    def __init__(self, notebook):
        self.tab = ttk.Frame(notebook)
        notebook.add(self.tab, text="Programs")
        self._build_ui()
        self.refresh()

    def _build_ui(self):
        frame = tk.Frame(self.tab)
        frame.pack(pady=10)

        self.entries = {}
        for i, field in enumerate(PROGRAM_FIELDS):
            tk.Label(frame, text=field.upper()).grid(row=0, column=i * 2, padx=5)
            entry = tk.Entry(frame)
            entry.grid(row=0, column=i * 2 + 1, padx=5)
            self.entries[field] = entry

        tk.Button(frame, text="Add", command=self.add).grid(row=1, column=0)
        tk.Button(frame, text="Delete", command=self.delete).grid(row=1, column=1)

        self.tree = ttk.Treeview(self.tab, columns=PROGRAM_FIELDS, show="headings")
        for col in PROGRAM_FIELDS:
            self.tree.heading(col, text=col.upper())
            self.tree.column(col, width=200)
        self.tree.pack(fill="both", expand=True)

    def refresh(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for p in load_data(PROGRAM_FILE):
            self.tree.insert("", tk.END, values=[p.get(f, "") for f in PROGRAM_FIELDS])

    def add(self):
        data = {f: self.entries[f].get().strip() for f in PROGRAM_FIELDS}

        if not any(c["code"] == data["college_code"] for c in load_data(COLLEGE_FILE)):
            messagebox.showerror("Error", "College does not exist.")
            return

        programs = load_data(PROGRAM_FILE)
        if any(p["code"] == data["code"] for p in programs):
            messagebox.showerror("Error", "Program code already exists.")
            return

        programs.append(data)
        save_data(PROGRAM_FILE, PROGRAM_FIELDS, programs)
        self.refresh()

    def delete(self):
        code = self.entries["code"].get().strip()

        if any(s["program_code"] == code for s in load_data(STUDENT_FILE)):
            messagebox.showerror("Error", "Cannot delete. Program has students.")
            return

        programs = [p for p in load_data(PROGRAM_FILE) if p["code"] != code]
        save_data(PROGRAM_FILE, PROGRAM_FIELDS, programs)
        self.refresh()
