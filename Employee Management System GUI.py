import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
import re
from datetime import date

# Database connection
con = mysql.connector.connect(
    host="localhost",
    user="root",
    password="sql.1",
    database="employee"
)

regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
phone_pattern = re.compile("(0|92|\\+92)?3[0-9]{9}")

# Main Application
class EmployeeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Employee Management System")
        self.root.geometry("900x600")
        self.root.configure(bg="#f0f4f7")

        title = tk.Label(self.root, text="Employee Management System", font=("Helvetica", 20, "bold"), bg="#2e86de", fg="white", pady=10)
        title.pack(fill=tk.X)

        # Scrollable Button Frame
        canvas_frame = tk.Frame(self.root)
        canvas_frame.pack(pady=10, fill=tk.BOTH, expand=True)

        canvas = tk.Canvas(canvas_frame, bg="#f0f4f7", highlightthickness=0)
        scrollbar = ttk.Scrollbar(canvas_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#f0f4f7")

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Buttons for each feature
        options = [
            ("Add Department", self.add_department_window),
            ("View Departments", self.view_departments_window),
            ("Add Employee", self.add_employee_window),
            ("View Employees", self.view_employees_window),
            ("Add Project", self.add_project_window),
            ("View Projects", self.view_projects_window),
            ("Assign Project", self.assign_project_window),
            ("View Assigned Project", self.view_project_assignments_window),
            ("Log Attendance", self.log_attendance_window),
            ("View Attendance", self.view_attendance_window),
            ("Search Employee", self.search_employee_window),
            ("Remove Employee", self.remove_employee_window),
            ("Promote Employee", self.promote_employee_window),
            ("Exit", self.root.quit)
        ]

        for index, (text, cmd) in enumerate(options):
            row = index // 2
            col = index % 2
            tk.Button(scrollable_frame, text=text, width=30, height=2,
                      bg="#48c9b0", fg="white", font=("Helvetica", 10, "bold"),
                      command=cmd).grid(row=row, column=col, padx=10, pady=5)

    def check_employee(self, emp_id):
        cur = con.cursor(buffered=True)
        cur.execute("SELECT * FROM empdata WHERE Id = %s", (emp_id,))
        return cur.rowcount == 1

    def add_employee_window(self):
        win = tk.Toplevel(self.root)
        win.title("Add Employee")
        win.geometry("400x600")
        win.configure(bg="white")

        labels = ["ID", "Name", "Email", "Phone", "Address", "Post", "Salary", "Department ID"]
        entries = []

        for i, label in enumerate(labels):
            tk.Label(win, text=label, bg="white", font=("Helvetica", 10)).pack(pady=5)
            ent = tk.Entry(win, width=30, font=("Helvetica", 10))
            ent.pack()
            entries.append(ent)

        def submit():
            Id, Name, Email, Phone, Address, Post, Salary, Dept_ID = [e.get() for e in entries]
            if self.check_employee(Id):
                messagebox.showerror("Error", "Employee ID already exists.")
                return
            if not re.fullmatch(regex, Email):
                messagebox.showerror("Error", "Invalid Email.")
                return
            if not phone_pattern.match(Phone):
                messagebox.showerror("Error", "Invalid Phone Number.")
                return
            sql = 'INSERT INTO empdata VALUES (%s,%s,%s,%s,%s,%s,%s,%s)'
            data = (Id, Name, Email, Phone, Address, Post, Salary, Dept_ID)
            cur = con.cursor()
            cur.execute(sql, data)
            con.commit()
            messagebox.showinfo("Success", "Employee Added Successfully")
            win.destroy()

        tk.Button(win, text="Submit", bg="#2ecc71", fg="white", font=("Helvetica", 10, "bold"), command=submit).pack(pady=10)

    def view_employees_window(self):
        win = tk.Toplevel(self.root)
        win.title("All Employees")
        win.geometry("900x400")

        tree = ttk.Treeview(win, columns=("ID", "Name", "Email", "Phone", "Address", "Post", "Salary", "Dept_ID"), show='headings')
        for col in tree["columns"]:
            tree.heading(col, text=col)
            tree.column(col, width=100)
        tree.pack(fill=tk.BOTH, expand=True)

        cur = con.cursor()
        cur.execute("SELECT * FROM empdata")
        for row in cur.fetchall():
            tree.insert("", tk.END, values=row)

    def search_employee_window(self):
        self._id_window("Search Employee", self._search_employee)

    def remove_employee_window(self):
        self._id_window("Remove Employee", self._remove_employee)

    def promote_employee_window(self):
        win = tk.Toplevel(self.root)
        win.title("Promote Employee")
        win.geometry("400x300")

        tk.Label(win, text="Employee ID:").pack(pady=5)
        emp_id_entry = tk.Entry(win)
        emp_id_entry.pack()

        tk.Label(win, text="New Salary:").pack(pady=5)
        salary_entry = tk.Entry(win)
        salary_entry.pack()

        tk.Label(win, text="New Post (optional):").pack(pady=5)
        post_entry = tk.Entry(win)
        post_entry.pack()

        def promote():
            emp_id = emp_id_entry.get()
            new_salary = salary_entry.get()
            new_post = post_entry.get()
            if not self.check_employee(emp_id):
                messagebox.showerror("Error", "Employee ID does not exist.")
                return
            cur = con.cursor()
            if new_post.strip():
                cur.execute("UPDATE empdata SET Salary=%s, Post=%s WHERE Id=%s", (new_salary, new_post, emp_id))
            else:
                cur.execute("UPDATE empdata SET Salary=%s WHERE Id=%s", (new_salary, emp_id))
            con.commit()
            messagebox.showinfo("Success", "Employee promoted successfully.")
            win.destroy()

        tk.Button(win, text="Promote", command=promote, bg="#2ecc71", fg="white").pack(pady=20)

    def _id_window(self, title, command):
        win = tk.Toplevel(self.root)
        win.title(title)
        win.geometry("300x150")

        tk.Label(win, text="Employee ID:").pack(pady=10)
        entry = tk.Entry(win)
        entry.pack()

        def submit():
            command(entry.get())
            win.destroy()

        tk.Button(win, text="Submit", command=submit, bg="#2ecc71", fg="white").pack(pady=10)

    def _search_employee(self, emp_id):
        cur = con.cursor()
        cur.execute("SELECT * FROM empdata WHERE Id = %s", (emp_id,))
        r = cur.fetchone()
        if r:
            info = "\n".join([
                f"Employee ID: {r[0]}",
                f"Name: {r[1]}",
                f"Email: {r[2]}",
                f"Phone: {r[3]}",
                f"Address: {r[4]}",
                f"Post: {r[5]}",
                f"Salary: {r[6]}",
                f"Department ID: {r[7]}"
            ])
            messagebox.showinfo("Employee Found", info)
        else:
            messagebox.showerror("Not Found", "No employee found with that ID.")

    def _remove_employee(self, emp_id):
        if not self.check_employee(emp_id):
            messagebox.showerror("Error", "Employee ID does not exist.")
            return
        cur = con.cursor()
        cur.execute("DELETE FROM empdata WHERE Id = %s", (emp_id,))
        con.commit()
        messagebox.showinfo("Success", "Employee removed successfully.")

    def add_department_window(self):
        self._form_window("Add Department", ["Department ID", "Department Name"],
                          lambda vals: self._db_insert("INSERT INTO department VALUES (%s, %s)", vals, "Department added."))

    def view_departments_window(self):
        win = tk.Toplevel(self.root)
        win.title("View Departments")
        win.geometry("500x300")

        tree = ttk.Treeview(win, columns=("Dept ID", "Dept Name"), show='headings')
        tree.heading("Dept ID", text="Department ID")
        tree.heading("Dept Name", text="Department Name")
        tree.column("Dept ID", width=150)
        tree.column("Dept Name", width=300)
        tree.pack(fill=tk.BOTH, expand=True)

        cur = con.cursor()
        cur.execute("SELECT * FROM department")
        for row in cur.fetchall():
            tree.insert("", tk.END, values=row)

    def add_project_window(self):
        self._form_window("Add Project", ["Project ID", "Project Name", "Start Date (YYYY-MM-DD)", "End Date (YYYY-MM-DD)"],
                          lambda vals: self._db_insert("INSERT INTO project VALUES (%s, %s, %s, %s)", vals, "Project added."))

    def assign_project_window(self):
        self._form_window("Assign Project", ["Employee ID", "Project ID", "Role"],
                          lambda vals: self._db_insert("INSERT INTO employee_project VALUES (%s, %s, %s)", vals, "Project assigned."))

    def log_attendance_window(self):
        self._form_window("Log Attendance", ["Employee ID", "Date (YYYY-MM-DD)", "Status (Present/Absent/Leave)"],
                          lambda vals: self._db_insert("INSERT INTO attendance (Emp_ID, Date, Status) VALUES (%s, %s, %s)", vals, "Attendance logged."))

    def view_projects_window(self):
        win = tk.Toplevel(self.root)
        win.title("View Projects")
        win.geometry("600x400")

        tree = ttk.Treeview(win, columns=("Project ID", "Name", "Start Date", "End Date"), show='headings')
        for col in tree["columns"]:
            tree.heading(col, text=col)
            tree.column(col, width=150)
        tree.pack(fill=tk.BOTH, expand=True)

        cur = con.cursor()
        cur.execute("SELECT * FROM project")
        for row in cur.fetchall():
            tree.insert("", tk.END, values=row)

    def view_project_assignments_window(self):
        win = tk.Toplevel(self.root)
        win.title("View Project Assignments")
        win.geometry("700x400")

        tree = ttk.Treeview(win, columns=("Emp ID", "Name", "Project ID", "Project Name", "Role"), show='headings')
        for col in tree["columns"]:
            tree.heading(col, text=col)
            tree.column(col, width=130)
        tree.pack(fill=tk.BOTH, expand=True)

        cur = con.cursor()
        cur.execute("""
            SELECT ep.Emp_ID, ed.Name, ep.Project_ID, p.Project_Name, ep.Role
            FROM employee_project ep
            JOIN empdata ed ON ep.Emp_ID = ed.Id
            JOIN project p ON ep.Project_ID = p.Project_ID
        """)
        for row in cur.fetchall():
            tree.insert("", tk.END, values=row)

    def view_attendance_window(self):
        win = tk.Toplevel(self.root)
        win.title("View Attendance")
        win.geometry("600x400")

        tree = ttk.Treeview(win, columns=("Attendance ID", "Emp ID", "Date", "Status"), show='headings')
        for col in tree["columns"]:
            tree.heading(col, text=col)
            tree.column(col, width=130)
        tree.pack(fill=tk.BOTH, expand=True)

        cur = con.cursor()
        cur.execute("SELECT * FROM attendance")
        for row in cur.fetchall():
            tree.insert("", tk.END, values=row)

    def _form_window(self, title, fields, on_submit):
        win = tk.Toplevel(self.root)
        win.title(title)
        win.geometry("400x500")
        entries = []

        for label in fields:
            tk.Label(win, text=label).pack(pady=5)
            ent = tk.Entry(win, width=30)
            ent.pack()
            entries.append(ent)

        def submit():
            values = [e.get() for e in entries]
            on_submit(values)
            win.destroy()

        tk.Button(win, text="Submit", command=submit, bg="#2ecc71", fg="white").pack(pady=20)

    def _db_insert(self, sql, data, success_msg):
        cur = con.cursor()
        cur.execute(sql, data)
        con.commit()
        messagebox.showinfo("Success", success_msg)

# Launch app
if __name__ == '__main__':
    root = tk.Tk()
    app = EmployeeApp(root)
    root.mainloop()
