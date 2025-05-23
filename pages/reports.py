import tkinter as tk
import tkinter.ttk as ttk
from pages.side_menu import SideMenu
from tkinter import messagebox

class ReportsPage(tk.Frame):
    def __init__(self, master, controller=None, username="admin"):
        super().__init__(master, bg="#D9D9D9")
        self.controller = controller
        self.username = username

        self.window_width = 1440
        self.window_height = 900
        self.sidebar_width = int(0.2 * self.window_width)

        # === Sidebar ===
        self.sidebar = SideMenu(self, controller=self.controller, active_page="Reports", username=username)
        self.sidebar.place(x=0, y=0)

        # === Main content area ===
        self.reports_area = tk.Frame(self, bg="#D9D9D9", width=self.window_width - self.sidebar_width, height=self.window_height)
        self.reports_area.place(x=self.sidebar_width, y=0)

        # === Page Title ===
        tk.Label(
            self.reports_area,
            text="Reports",
            font=("Poppins", 24, "bold"),
            bg="#D9D9D9",
            fg="#222"
        ).place(x=30, y=15)

        # === Top-right user label ===
        x_start = self.window_width - self.sidebar_width - 200
        tk.Label(self.reports_area, text="Logged in as:", font=("Poppins", 11), fg="#333", bg="#D9D9D9").place(x=x_start, y=20)
        tk.Label(self.reports_area, text=self.username, font=("Poppins", 12, "bold"), fg="#333", bg="#D9D9D9").place(x=x_start + 110, y=19)

        # === Table and Controls ===
        self.create_test_table()
        self.create_button_panel()

        print("✅ ReportsPage rendered with sidebar, table, and buttons.")

    def create_test_table(self):
        columns = ("serial", "name", "type", "date", "time", "notes")

        style = ttk.Style()
        style.configure("Treeview.Heading", font=("Poppins", 11, "bold"), background="white", foreground="#333")
        style.configure("Treeview", font=("Poppins", 10), rowheight=28, borderwidth=1)

        self.test_table = ttk.Treeview(
            self.reports_area,
            columns=columns,
            show="headings",
            height=15,
            style="Treeview"
        )

        for col, text in zip(columns, ["Serial No.", "Test Name", "Test Type", "Date", "Time", "Notes"]):
            self.test_table.heading(col, text=text)

        self.test_table.column("serial", width=80, anchor="center")
        self.test_table.column("name", width=160, anchor="center")
        self.test_table.column("type", width=120, anchor="center")
        self.test_table.column("date", width=100, anchor="center")
        self.test_table.column("time", width=100, anchor="center")
        self.test_table.column("notes", width=300)

        self.test_table.place(x=30, y=150, width=1000, height=550)

        # === Scrollbar ===
        scrollbar = ttk.Scrollbar(self.reports_area, orient="vertical", command=self.test_table.yview)
        self.test_table.configure(yscrollcommand=scrollbar.set)
        scrollbar.place(x=1030, y=150, height=550)

        # === Tag styles for alternating rows
        self.test_table.tag_configure("row_even", background="#C1D5EA")
        self.test_table.tag_configure("row_odd", background="#DEEAF5")
        self.test_table.bind("<Motion>", self.on_row_hover)

        sample_data = [
            (1, "Leak Test 1", "Leak", "2025-05-22", "14:03", "Passed visual inspection."),
            (2, "Pressure Drop", "PDD", "2025-05-20", "10:45", "Noted irregular drop."),
            (3, "Valve Test A", "Gas", "2025-05-18", "09:30", "Needs retesting."),
            (4, "System Flow", "Gas", "2025-05-17", "12:10", "Stable."),
            (5, "Final Test", "Leak", "2025-05-16", "11:00", "All metrics passed.")
        ]

        for i, row in enumerate(sample_data):
            tag = "row_even" if i % 2 == 0 else "row_odd"
            self.test_table.insert("", "end", values=row, tags=(tag,))

    def create_button_panel(self):
        # Delete button aligned with right side of table
        delete_btn = tk.Button(self.reports_area, text="Delete Row", font=("Poppins", 10), command=self.delete_selected_row)
        delete_btn.place(x=950, y=100, width=100)

        # Edit button to the left of Delete
        edit_btn = tk.Button(self.reports_area, text="Edit Row", font=("Poppins", 10), command=self.edit_selected_row)
        edit_btn.place(x=840, y=100, width=100)

    def delete_selected_row(self):
        selected = self.test_table.selection()
        if not selected:
            messagebox.showwarning("No Selection", "Please select a row to delete.")
            return

        confirm = messagebox.askyesno("Delete Row", "Are you sure you want to delete the selected row?")
        if confirm:
            self.test_table.delete(selected[0])

    def edit_selected_row(self):
        selected = self.test_table.selection()
        if not selected:
            messagebox.showwarning("No Selection", "Please select a row to edit.")
            return

        row_id = selected[0]
        values = self.test_table.item(row_id, "values")

        # === Popup edit window
        popup = tk.Toplevel(self)
        popup.title("Edit Row")
        popup.geometry("400x400")
        popup.configure(bg="white")

        entries = []
        labels = ["Serial No.", "Test Name", "Test Type", "Date", "Time", "Notes"]

        for i, label_text in enumerate(labels):
            tk.Label(popup, text=label_text, font=("Poppins", 10), bg="white").pack(pady=(10 if i == 0 else 5, 0))
            entry = tk.Entry(popup, font=("Poppins", 10), width=40)
            entry.insert(0, values[i])
            entry.pack()
            entries.append(entry)

        def save_changes():
            new_values = [e.get() for e in entries]
            self.test_table.item(row_id, values=new_values)
            popup.destroy()

        tk.Button(popup, text="Save", font=("Poppins", 10, "bold"), command=save_changes).pack(pady=20)

    def on_row_hover(self, event):
        row_id = self.test_table.identify_row(event.y)
        region = self.test_table.identify("region", event.x, event.y)

        for item in self.test_table.get_children():
            index = int(self.test_table.index(item))
            tag = "row_even" if index % 2 == 0 else "row_odd"
            self.test_table.item(item, tags=(tag,))

        if region == "cell" and row_id:
            self.test_table.item(row_id, tags=("hover",))
            self.test_table.tag_configure("hover", background="#B0C4DE")
