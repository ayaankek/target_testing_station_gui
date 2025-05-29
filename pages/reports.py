import tkinter as tk
import tkinter.ttk as ttk
import csv
import matplotlib.pyplot as plt

from pages.side_menu import SideMenu
from tkinter import messagebox
from tkinter import filedialog
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from datetime import timedelta
from tempfile import NamedTemporaryFile

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
        columns = ("serial", "name", "type", "date", "time", "notes", "start_seconds")

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

        for col, text in zip(columns, ["Serial No.", "Test Name", "Test Type", "Date", "Duration", "Notes"]):
            self.test_table.heading(col, text=text)

        self.test_table.column("serial", width=80, anchor="center")
        self.test_table.column("name", width=160, anchor="center")
        self.test_table.column("type", width=120, anchor="center")
        self.test_table.column("date", width=100, anchor="center")
        self.test_table.column("time", width=100, anchor="center")
        self.test_table.column("notes", width=300)
        self.test_table.column("start_seconds", width=0, anchor="center")

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
            (1, "Leak Test 1", "Leak", "2025-05-22", "5m 32s", "Passed visual inspection."),
            (2, "Pressure Drop", "PDD", "2025-05-20", "12m 5s", "Noted irregular drop."),
            (3, "Valve Test A", "Gas", "2025-05-18", "3m 47s", "Needs retesting."),
            (4, "System Flow", "Gas", "2025-05-17", "7m 59s", "Stable."),
            (5, "Final Test", "Leak", "2025-05-16", "10m 18s", "All metrics passed.")
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

        # === Export Buttons ===
        export_csv_btn = tk.Button(self.reports_area, text="Export to CSV", font=("Poppins", 10), command=self.export_to_csv)
        export_csv_btn.place(x=790, y=720, width=120)

        export_pdf_btn = tk.Button(self.reports_area, text="Export to PDF", font=("Poppins", 10), command=self.export_to_pdf)
        export_pdf_btn.place(x=930, y=720, width=120)

        log_btn = tk.Button(self.reports_area, text="Log Test Data", font=("Poppins", 10), command=self.open_log_prompt)
        log_btn.place(x=700, y=100, width=120)

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
        popup.geometry("420x460")
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

    def export_to_csv(self):
        selected = self.test_table.selection()
        if not selected:
            messagebox.showwarning("No Selection", "Please select a row to export.")
            return

        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV Files", "*.csv")])
        if not file_path:
            return

        row = self.test_table.item(selected[0])['values']
        test_name, duration = row[1], row[4]

        # Get full chamber data from controller (LiveDataPage must define get_chamber_data)
        full_data = self.controller.get_chamber_data()

        start_seconds = int(row[6])  # stored in hidden column
        filtered_data = [(t, p, temp) for t, p, temp in full_data if t >= start_seconds]
        shifted_data = [(t - start_seconds, p, temp) for t, p, temp in filtered_data]

        # (Optional) You could filter the chamber_data based on the duration
        # For now, we assume you want to export the entire chamber_data

        with open(file_path, mode="w", newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["Test Info"])
            writer.writerow(["Serial No.", "Test Name", "Test Type", "Date", "Duration", "Notes"])
            writer.writerow(row)

            writer.writerow([])  # empty line
            writer.writerow(["Chamber Data"])
            writer.writerow(["Time (s)", "Pressure (Pa)", "Temperature (°C)"])
            for t, p, temp in shifted_data:
                writer.writerow([t, p, temp])

        messagebox.showinfo("Export Complete", f"Data exported to {file_path}")

    def export_to_pdf(self):
        selected = self.test_table.selection()
        if not selected:
            messagebox.showwarning("No Selection", "Please select a row to export.")
            return

        file_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF Files", "*.pdf")])
        if not file_path:
            return

        from datetime import datetime
        c = canvas.Canvas(file_path, pagesize=letter)
        width, height = letter

        c.setFont("Helvetica-Bold", 14)
        c.drawString(30, height - 50, "Test Report Export")

        # Draw selected test row info
        c.setFont("Helvetica-Bold", 10)
        headers = ["Serial No.", "Test Name", "Test Type", "Date", "Duration", "Notes"]
        y = height - 80
        for i, header in enumerate(headers):
            c.drawString(30 + i * 90, y, header)

        c.setFont("Helvetica", 9)
        y -= 20
        row = self.test_table.item(selected[0])['values']
        for i, value in enumerate(row):
            c.drawString(30 + i * 90, y, str(value))

        # Add chamber data
        y -= 40
        c.setFont("Helvetica-Bold", 11)
        c.drawString(30, y, "Chamber Data")
        y -= 20
        c.setFont("Helvetica-Bold", 9)
        c.drawString(30, y, "Time (s)")
        c.drawString(130, y, "Pressure (Pa)")
        c.drawString(240, y, "Temperature (°C)")

        y -= 20
        c.setFont("Helvetica", 9)

        # Pull chamber data from LiveDataPage via controller
        full_data = self.controller.get_chamber_data()
        start_seconds = int(row[6])
        filtered_data = [(t, p, temp) for t, p, temp in full_data if t >= start_seconds]
        shifted_data = [(t - start_seconds, p, temp) for t, p, temp in filtered_data]

        for t, p, temp in shifted_data:
            c.drawString(30, y, f"{t:.2f}")
            c.drawString(130, y, f"{p:.2f}")
            c.drawString(240, y, f"{temp:.2f}")

            y -= 15
            if y < 50:
                c.showPage()
                y = height - 50
                c.setFont("Helvetica", 9)

        c.save()
        messagebox.showinfo("Export Complete", f"PDF saved to {file_path}")

    def open_log_prompt(self):
        popup = tk.Toplevel(self)
        popup.title("Log Test Data")
        popup.geometry("420x380")
        popup.configure(bg="white")

        tk.Label(popup, text="Log Chamber Data", font=("Poppins", 14, "bold"), bg="white").pack(pady=10)

        # === Test Name ===
        tk.Label(popup, text="Test Name:", font=("Poppins", 10), bg="white").pack(anchor="w", padx=30, pady=(5, 0))
        name_entry = tk.Entry(popup, font=("Poppins", 10), width=35)
        name_entry.pack(pady=5)

        # === Notes ===
        tk.Label(popup, text="Notes (optional):", font=("Poppins", 10), bg="white").pack(anchor="w", padx=30, pady=(5, 0))
        notes_entry = tk.Entry(popup, font=("Poppins", 10), width=35)
        notes_entry.pack(pady=5)

        # === Start Time ===
        tk.Label(popup, text="Start Time (HH:MM:SS):", font=("Poppins", 10), bg="white").pack(anchor="w", padx=30, pady=(10, 0))
        start_entry = tk.Entry(popup, font=("Poppins", 10), width=35)
        start_entry.pack(pady=5)

        # === End Time ===
        tk.Label(popup, text="End Time (HH:MM:SS):", font=("Poppins", 10), bg="white").pack(anchor="w", padx=30, pady=(5, 0))
        end_entry = tk.Entry(popup, font=("Poppins", 10), width=35)
        end_entry.pack(pady=5)

        # === Submit Button ===
        def start_logging():
            def hms_to_seconds(hms_str):
                h, m, s = map(int, hms_str.split(":"))
                return h * 3600 + m * 60 + s
            
            def valid_time_format(s):
                try:
                    h, m, s = map(int, s.split(":"))
                    return True
                except:
                    return False
            
            test_name = name_entry.get().strip()
            notes = notes_entry.get().strip()
            start_time = start_entry.get().strip()
            end_time = end_entry.get().strip()
            start_seconds = hms_to_seconds(start_time)
            end_seconds = hms_to_seconds(end_time)

            if not test_name or not start_time or not end_time:
                messagebox.showerror("Missing Info", "Please fill in test name, start time, and end time.")
                return

            if not (valid_time_format(start_time) and valid_time_format(end_time)):
                messagebox.showerror("Invalid Format", "Times must be in HH:MM:SS format.")
                return

            # === Format duration from start and end
            from datetime import timedelta

            def parse_time(tstr):
                h, m, s = map(int, tstr.split(":"))
                return timedelta(hours=h, minutes=m, seconds=s)

            t1 = parse_time(start_time)
            t2 = parse_time(end_time)

            if t2 <= t1:
                messagebox.showerror("Invalid Range", "End time must be after start time.")
                return

            duration_str = str(t2 - t1)

            # === Add to table
            from datetime import datetime
            date_str = datetime.now().strftime("%Y-%m-%d")
            serial = len(self.test_table.get_children()) + 1

            row = (serial, test_name, "Chamber", date_str, duration_str, notes, start_seconds)
            tag = "row_even" if serial % 2 == 0 else "row_odd"
            self.test_table.insert("", "end", values=row, tags=(tag,))

            popup.destroy()
            messagebox.showinfo("Logged", f"New log '{test_name}' added.")
        
        tk.Label(popup, text="").pack()  # spacer
        tk.Button(popup, text="Submit", font=("Poppins", 10, "bold"), command=start_logging).pack(pady=20)
        popup.update_idletasks()  # force geometry recalculation

        # === Dynamically resize popup to fit all widgets ===
        popup.update_idletasks()
        popup.geometry(f"420x{popup.winfo_reqheight()}")  # force height = content height
        popup.resizable(False, False)
    
    def parse_duration(duration_str):
        try:
            parts = duration_str.strip().split(":")
            if len(parts) != 3:
                return None
            h, m, s = map(int, parts)
            if not (0 <= m < 60 and 0 <= s < 60):
                return None
            return timedelta(hours=h, minutes=m, seconds=s)
        except:
            return None