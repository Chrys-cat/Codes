"""
Simple Student Information System				
Using only csv files.					
student
- id  format: YYYY-NNNN
- firstname
- lastname
- program code=> refers to program table
- year
- gender

program
- code  e.g. BSCS
- name e.g. Bachelor of Science in Computer Science
- college => refers to college table

college
- code e.g. CCS
- name e.g. College of Computer Studies

Should have the ff:
- CRUDL for students, program and college
- sort
 - search by fields
"""
print('wow')










import csv
import os
import re
import tkinter as tk
from tkinter import ttk, messagebox

# ---------------- FILE CONFIG ---------------- #

STUDENT_FILE = "students.csv"
PROGRAM_FILE = "programs.csv"
COLLEGE_FILE = "colleges.csv"

STUDENT_FIELDS = ["id","firstname","lastname","program_code","year","gender"]
PROGRAM_FIELDS = ["code","name","college_code"]
COLLEGE_FIELDS = ["code","name"]

# ---------------- UTILITIES ---------------- #

def ensure_file(filename, headers):
    if not os.path.exists(filename):
        with open(filename, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(headers)

def load_data(filename):
    if not os.path.exists(filename):
        return []
    with open(filename, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))

def save_data(filename, fieldnames, data):
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)

def valid_student_id(sid):
    return re.match(r"^\d{4}-\d{4}$", sid)

# ---------------- GUI APP ---------------- #

class SISApp:

    def __init__(self, root):
        self.root = root
        self.root.title("Student Information System")
        self.root.geometry("1000x600")

        ensure_file(STUDENT_FILE, STUDENT_FIELDS)
        ensure_file(PROGRAM_FILE, PROGRAM_FIELDS)
        ensure_file(COLLEGE_FILE, COLLEGE_FIELDS)

        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill="both", expand=True)

        self.create_student_tab()
        self.create_program_tab()
        self.create_college_tab()

    # =====================================================
    # STUDENT TAB
    # =====================================================

    def create_student_tab(self):
        self.student_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.student_tab, text="Students")

        frame = tk.Frame(self.student_tab)
        frame.pack(pady=10)

        labels = ["ID (YYYY-NNNN)", "First Name", "Last Name",
                  "Program Code", "Year", "Gender"]

        self.student_entries = {}

        for i, label in enumerate(labels):
            tk.Label(frame, text=label).grid(row=i//3, column=(i%3)*2, padx=5, pady=5)
            entry = tk.Entry(frame)
            entry.grid(row=i//3, column=(i%3)*2+1, padx=5)
            self.student_entries[STUDENT_FIELDS[i]] = entry

        btn_frame = tk.Frame(self.student_tab)
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="Add", command=self.add_student).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Update", command=self.update_student).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Delete", command=self.delete_student).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Search", command=self.search_student).pack(side="left", padx=5)

        self.student_tree = ttk.Treeview(self.student_tab, columns=STUDENT_FIELDS, show="headings")
        for col in STUDENT_FIELDS:
            self.student_tree.heading(col, text=col.upper())
            self.student_tree.column(col, width=140)
        self.student_tree.pack(fill="both", expand=True)
        self.student_tree.bind("<<TreeviewSelect>>", self.fill_student_fields)

        self.refresh_students()

    def refresh_students(self):
        for row in self.student_tree.get_children():
            self.student_tree.delete(row)

        for s in load_data(STUDENT_FILE):
            row = [s.get(f, "") for f in STUDENT_FIELDS]
            self.student_tree.insert("", tk.END, values=row)

    def clear_student_fields(self):
        for entry in self.student_entries.values():
            entry.delete(0, tk.END)

    def add_student(self):
        data = {f: self.student_entries[f].get().strip() for f in STUDENT_FIELDS}

        if not valid_student_id(data["id"]):
            messagebox.showerror("Error", "Invalid ID format (YYYY-NNNN).")
            return

        programs = load_data(PROGRAM_FILE)
        if not any(p["code"] == data["program_code"] for p in programs):
            messagebox.showerror("Error", "Program does not exist.")
            return

        students = load_data(STUDENT_FILE)
        if any(s["id"] == data["id"] for s in students):
            messagebox.showerror("Error", "Student ID already exists.")
            return

        students.append(data)
        save_data(STUDENT_FILE, STUDENT_FIELDS, students)
        self.refresh_students()
        self.clear_student_fields()

    def update_student(self):
        data = {f: self.student_entries[f].get().strip() for f in STUDENT_FIELDS}
        students = load_data(STUDENT_FILE)

        if not any(p["code"] == data["program_code"] for p in load_data(PROGRAM_FILE)):
            messagebox.showerror("Error", "Program does not exist.")
            return

        for s in students:
            if s["id"] == data["id"]:
                s.update(data)
                save_data(STUDENT_FILE, STUDENT_FIELDS, students)
                self.refresh_students()
                return

        messagebox.showerror("Error", "Student not found.")

    def delete_student(self):
        sid = self.student_entries["id"].get()
        students = load_data(STUDENT_FILE)
        students = [s for s in students if s["id"] != sid]
        save_data(STUDENT_FILE, STUDENT_FIELDS, students)
        self.refresh_students()
        self.clear_student_fields()

    def search_student(self):
        sid = self.student_entries["id"].get()
        for s in load_data(STUDENT_FILE):
            if s["id"] == sid:
                for f in STUDENT_FIELDS:
                    self.student_entries[f].delete(0, tk.END)
                    self.student_entries[f].insert(0, s[f])
                return
        messagebox.showinfo("Search", "Student not found.")

    def fill_student_fields(self, event):
        selected = self.student_tree.focus()
        if not selected:
            return
        values = self.student_tree.item(selected, "values")
        for i, field in enumerate(STUDENT_FIELDS):
            self.student_entries[field].delete(0, tk.END)
            self.student_entries[field].insert(0, values[i])

    # =====================================================
    # PROGRAM TAB
    # =====================================================

    def create_program_tab(self):
        self.program_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.program_tab, text="Programs")

        frame = tk.Frame(self.program_tab)
        frame.pack(pady=10)

        self.program_entries = {}
        for i, field in enumerate(PROGRAM_FIELDS):
            tk.Label(frame, text=field.upper()).grid(row=0, column=i*2, padx=5)
            entry = tk.Entry(frame)
            entry.grid(row=0, column=i*2+1, padx=5)
            self.program_entries[field] = entry

        tk.Button(frame, text="Add", command=self.add_program).grid(row=1, column=0)
        tk.Button(frame, text="Delete", command=self.delete_program).grid(row=1, column=1)

        self.program_tree = ttk.Treeview(self.program_tab, columns=PROGRAM_FIELDS, show="headings")
        for col in PROGRAM_FIELDS:
            self.program_tree.heading(col, text=col.upper())
            self.program_tree.column(col, width=200)
        self.program_tree.pack(fill="both", expand=True)

        self.refresh_programs()

    def refresh_programs(self):
        for row in self.program_tree.get_children():
            self.program_tree.delete(row)
        for p in load_data(PROGRAM_FILE):
            row = [p.get(f, "") for f in PROGRAM_FIELDS]
            self.program_tree.insert("", tk.END, values=row)

    def add_program(self):
        data = {f: self.program_entries[f].get().strip() for f in PROGRAM_FIELDS}

        colleges = load_data(COLLEGE_FILE)
        if not any(c["code"] == data["college_code"] for c in colleges):
            messagebox.showerror("Error", "College does not exist.")
            return

        programs = load_data(PROGRAM_FILE)
        if any(p["code"] == data["code"] for p in programs):
            messagebox.showerror("Error", "Program code already exists.")
            return

        programs.append(data)
        save_data(PROGRAM_FILE, PROGRAM_FIELDS, programs)
        self.refresh_programs()

    def delete_program(self):
        code = self.program_entries["code"].get()

        students = load_data(STUDENT_FILE)
        if any(s["program_code"] == code for s in students):
            messagebox.showerror("Error", "Cannot delete. Program has students.")
            return

        programs = load_data(PROGRAM_FILE)
        programs = [p for p in programs if p["code"] != code]
        save_data(PROGRAM_FILE, PROGRAM_FIELDS, programs)
        self.refresh_programs()

    # =====================================================
    # COLLEGE TAB
    # =====================================================

    def create_college_tab(self):
        self.college_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.college_tab, text="Colleges")

        frame = tk.Frame(self.college_tab)
        frame.pack(pady=10)

        self.college_entries = {}
        for i, field in enumerate(COLLEGE_FIELDS):
            tk.Label(frame, text=field.upper()).grid(row=0, column=i*2, padx=5)
            entry = tk.Entry(frame)
            entry.grid(row=0, column=i*2+1, padx=5)
            self.college_entries[field] = entry

        tk.Button(frame, text="Add", command=self.add_college).grid(row=1, column=0)
        tk.Button(frame, text="Delete", command=self.delete_college).grid(row=1, column=1)

        self.college_tree = ttk.Treeview(self.college_tab, columns=COLLEGE_FIELDS, show="headings")
        for col in COLLEGE_FIELDS:
            self.college_tree.heading(col, text=col.upper())
            self.college_tree.column(col, width=250)
        self.college_tree.pack(fill="both", expand=True)

        self.refresh_colleges()

    def refresh_colleges(self):
        for row in self.college_tree.get_children():
            self.college_tree.delete(row)
        for c in load_data(COLLEGE_FILE):
            row = [c.get(f, "") for f in COLLEGE_FIELDS]
            self.college_tree.insert("", tk.END, values=row)

    def add_college(self):
        data = {f: self.college_entries[f].get().strip() for f in COLLEGE_FIELDS}

        colleges = load_data(COLLEGE_FILE)
        if any(c["code"] == data["code"] for c in colleges):
            messagebox.showerror("Error", "College code already exists.")
            return

        colleges.append(data)
        save_data(COLLEGE_FILE, COLLEGE_FIELDS, colleges)
        self.refresh_colleges()

    def delete_college(self):
        code = self.college_entries["code"].get()

        programs = load_data(PROGRAM_FILE)
        if any(p["college_code"] == code for p in programs):
            messagebox.showerror("Error", "Cannot delete. College has programs.")
            return

        colleges = load_data(COLLEGE_FILE)
        colleges = [c for c in colleges if c["code"] != code]
        save_data(COLLEGE_FILE, COLLEGE_FIELDS, colleges)
        self.refresh_colleges()

# ---------------- RUN APP ---------------- #

if __name__ == "__main__":
    root = tk.Tk()
    app = SISApp(root)
    root.mainloop()