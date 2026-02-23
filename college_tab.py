import tkinter as tk
from tkinter import ttk, messagebox

from config import COLLEGE_FILE, COLLEGE_FIELDS, PROGRAM_FILE, PROGRAM_FIELDS
from utils import load_data, save_data


class CollegeTab:

    def __init__(self, notebook):
        self.tab = ttk.Frame(notebook)
        notebook.add(self.tab, text="Colleges")
        self._build_ui()
        self.refresh()

    def _build_ui(self):
        frame = tk.Frame(self.tab)
        frame.pack(pady=10)

        self.entries = {}
        for i, field in enumerate(COLLEGE_FIELDS):
            tk.Label(frame, text=field.upper()).grid(row=0, column=i * 2, padx=5)
            entry = tk.Entry(frame)
            entry.grid(row=0, column=i * 2 + 1, padx=5)
            self.entries[field] = entry

        tk.Button(frame, text="Add", command=self.add).grid(row=1, column=0)
        tk.Button(frame, text="Delete", command=self.delete).grid(row=1, column=1)

        self.tree = ttk.Treeview(self.tab, columns=COLLEGE_FIELDS, show="headings")
        for col in COLLEGE_FIELDS:
            self.tree.heading(col, text=col.upper())
            self.tree.column(col, width=250)
        self.tree.pack(fill="both", expand=True)

    def refresh(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for c in load_data(COLLEGE_FILE):
            self.tree.insert("", tk.END, values=[c.get(f, "") for f in COLLEGE_FIELDS])

    def add(self):
        data = {f: self.entries[f].get().strip() for f in COLLEGE_FIELDS}

        colleges = load_data(COLLEGE_FILE)
        if any(c["code"] == data["code"] for c in colleges):
            messagebox.showerror("Error", "College code already exists.")
            return

        colleges.append(data)
        save_data(COLLEGE_FILE, COLLEGE_FIELDS, colleges)
        self.refresh()

    def delete(self):
        code = self.entries["code"].get().strip()

        if any(p["college_code"] == code for p in load_data(PROGRAM_FILE)):
            messagebox.showerror("Error", "Cannot delete. College has programs.")
            return

        colleges = [c for c in load_data(COLLEGE_FILE) if c["code"] != code]
        save_data(COLLEGE_FILE, COLLEGE_FIELDS, colleges)
        self.refresh()
