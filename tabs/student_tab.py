import tkinter as tk
from tkinter import ttk, messagebox

from config import STUDENT_FILE, STUDENT_FIELDS, PROGRAM_FILE
from utils import load_data, save_data, valid_student_id


class StudentTab:

    def __init__(self, notebook):
        self.tab = ttk.Frame(notebook)
        notebook.add(self.tab, text="Students")
        self._build_ui()
        self.refresh()

    def _build_ui(self):
        frame = tk.Frame(self.tab)
        frame.pack(pady=10)

        labels = ["ID (YYYY-NNNN)", "First Name", "Last Name",
                  "Program Code", "Year", "Gender"]

        self.entries = {}
        for i, label in enumerate(labels):
            tk.Label(frame, text=label).grid(row=i // 3, column=(i % 3) * 2, padx=5, pady=5)
            entry = tk.Entry(frame)
            entry.grid(row=i // 3, column=(i % 3) * 2 + 1, padx=5)
            self.entries[STUDENT_FIELDS[i]] = entry

        btn_frame = tk.Frame(self.tab)
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="Add",    command=self.add).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Update", command=self.update).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Delete", command=self.delete).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Search", command=self.search).pack(side="left", padx=5)

        self.tree = ttk.Treeview(self.tab, columns=STUDENT_FIELDS, show="headings")
        for col in STUDENT_FIELDS:
            self.tree.heading(col, text=col.upper())
            self.tree.column(col, width=140)
        self.tree.pack(fill="both", expand=True)
        self.tree.bind("<<TreeviewSelect>>", self._on_select)

    def refresh(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for s in load_data(STUDENT_FILE):
            self.tree.insert("", tk.END, values=[s.get(f, "") for f in STUDENT_FIELDS])

    def _clear(self):
        for entry in self.entries.values():
            entry.delete(0, tk.END)

    def _get_data(self):
        return {f: self.entries[f].get().strip() for f in STUDENT_FIELDS}

    def _on_select(self, event):
        selected = self.tree.focus()
        if not selected:
            return
        values = self.tree.item(selected, "values")
        for i, field in enumerate(STUDENT_FIELDS):
            self.entries[field].delete(0, tk.END)
            self.entries[field].insert(0, values[i])

    def add(self):
        data = self._get_data()

        if not valid_student_id(data["id"]):
            messagebox.showerror("Error", "Invalid ID format (YYYY-NNNN).")
            return

        if not any(p["code"] == data["program_code"] for p in load_data(PROGRAM_FILE)):
            messagebox.showerror("Error", "Program does not exist.")
            return

        students = load_data(STUDENT_FILE)
        if any(s["id"] == data["id"] for s in students):
            messagebox.showerror("Error", "Student ID already exists.")
            return

        students.append(data)
        save_data(STUDENT_FILE, STUDENT_FIELDS, students)
        self.refresh()
        self._clear()

    def update(self):
        data = self._get_data()

        if not any(p["code"] == data["program_code"] for p in load_data(PROGRAM_FILE)):
            messagebox.showerror("Error", "Program does not exist.")
            return

        students = load_data(STUDENT_FILE)
        for s in students:
            if s["id"] == data["id"]:
                s.update(data)
                save_data(STUDENT_FILE, STUDENT_FIELDS, students)
                self.refresh()
                return

        messagebox.showerror("Error", "Student not found.")

    def delete(self):
        sid = self.entries["id"].get().strip()
        students = [s for s in load_data(STUDENT_FILE) if s["id"] != sid]
        save_data(STUDENT_FILE, STUDENT_FIELDS, students)
        self.refresh()
        self._clear()

    def search(self):
        sid = self.entries["id"].get().strip()
        for s in load_data(STUDENT_FILE):
            if s["id"] == sid:
                for f in STUDENT_FIELDS:
                    self.entries[f].delete(0, tk.END)
                    self.entries[f].insert(0, s[f])
                return
        messagebox.showinfo("Search", "Student not found.")
