import tkinter as tk
import tkinter.ttk as ttk
import csv
import matplotlib.pyplot as plt

from pages.side_menu import SideMenu
from tkinter import messagebox, filedialog
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from datetime import datetime, timedelta


class ReportsPage(tk.Frame):
    def __init__(self, master, controller=None, username="admin"):
        super().__init__(master, bg="#D9D9D9")
        self.controller = controller
        self.username = username
        self.window_width = 1440
        self.window_height = 900
        self.sidebar_width = int(0.2 * self.window_width)

        self.sidebar = SideMenu(self, controller=self.controller, active_page="Reports", username=username)
        self.sidebar.place(x=0, y=0)

        self.reports_area = tk.Frame(self, bg="#D9D9D9", width=self.window_width - self.sidebar_width, height=self.window_height)
        self.reports_area.place(x=self.sidebar_width, y=0)

        tk.Label(self.reports_area, text="Reports", font=("Poppins", 24, "bold"), bg="#D9D9D9", fg="#222").place(x=30, y=15)

        x_start = self.window_width - self.sidebar_width - 200
        tk.Label(self.reports_area, text="Logged in as:", font=("Poppins", 11), fg="#333", bg="#D9D9D9").place(x=x_start, y=20)
        tk.Label(self.reports_area, text=self.username, font=("Poppins", 12, "bold"), fg="#333", bg="#D9D9D9").place(x=x_start + 110, y=19)

        self.create_test_table()
        self.create_button_panel()

    def create_test_table(self):
        columns = (
            "serial", "target_name", "type", "date", "time",
            "target_pressure", "min_pressure", "max_pressure",
            "notes", "start_seconds"
        )

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

        headings = [
            "Serial No.", "Target Name", "Test Type", "Date", "Duration",
            "Target Pressure", "Min Pressure", "Max Pressure", "Notes"
        ]
        widths = [120, 140, 100, 100, 100, 120, 120, 120, 300, 0]

        for col, text, w in zip(columns, headings + [""], widths):  # headings has 9, columns has 10
            self.test_table.heading(col, text=text)
            self.test_table.column(col, width=w, anchor="center" if w else "w", stretch=False)

        # Place Treeview and Scrollbars
        self.test_table.place(x=30, y=150, width=1000, height=550)

        v_scroll = ttk.Scrollbar(self.reports_area, orient="vertical", command=self.test_table.yview)
        h_scroll = ttk.Scrollbar(self.reports_area, orient="horizontal", command=self.test_table.xview)

        self.test_table.configure(yscrollcommand=v_scroll.set, xscrollcommand=h_scroll.set)

        v_scroll.place(x=1030, y=150, height=550)
        h_scroll.place(x=30, y=700, width=1000)

        # Alternating row styles
        self.test_table.tag_configure("row_even", background="#C1D5EA")
        self.test_table.tag_configure("row_odd", background="#DEEAF5")
        self.test_table.bind("<Motion>", self.on_row_hover)

        sample_data = [
            ("SN-001", "SN-001, 2025-05-01, 00:04:32, 100.0 psi", "Leak", "2025-05-01", "00:04:32", "100.0", "98.2", "101.4", "Minor fluctuation observed", 0),
            ("SN-002", "SN-002, 2025-05-02, 00:08:15, 120.0 psi", "PDD", "2025-05-02", "00:08:15", "120.0", "115.6", "121.9", "Stable pressure decay", 0),
            ("SN-003", "SN-003, 2025-05-04, 00:02:45, 90.0 psi", "Gas", "2025-05-04", "00:02:45", "90.0", "89.0", "91.0", "Fast stabilization", 0),
            ("SN-004", "SN-004, 2025-05-06, 00:05:20, 105.0 psi", "Leak", "2025-05-06", "00:05:20", "105.0", "100.3", "106.7", "Slight initial leak", 0),
            ("SN-005", "SN-005, 2025-05-09, 00:09:05, 115.0 psi", "PDD", "2025-05-09", "00:09:05", "115.0", "110.2", "117.8", "Requires re-evaluation", 0),
            ("SN-006", "SN-006, 2025-05-10, 00:06:58, 130.0 psi", "Chamber", "2025-05-10", "00:06:58", "130.0", "128.0", "131.2", "Nominal behavior", 0),
            ("SN-007", "SN-007, 2025-05-12, 00:03:33, 95.0 psi", "Gas", "2025-05-12", "00:03:33", "95.0", "93.5", "96.1", "Logged by tech", 0)
        ]

        for i, row in enumerate(sample_data):
            tag = "row_even" if i % 2 == 0 else "row_odd"
            self.test_table.insert("", "end", values=row, tags=(tag,))

    def create_button_panel(self):
        tk.Button(self.reports_area, text="Log Test Data", font=("Poppins", 10), command=self.open_log_prompt).place(x=700, y=100, width=120)
        tk.Button(self.reports_area, text="Edit Row", font=("Poppins", 10), command=self.edit_selected_row).place(x=840, y=100, width=100)
        tk.Button(self.reports_area, text="Delete Row", font=("Poppins", 10), command=self.delete_selected_row).place(x=950, y=100, width=100)
        tk.Button(self.reports_area, text="Export to CSV", font=("Poppins", 10), command=self.export_to_csv).place(x=790, y=730, width=120)
        tk.Button(self.reports_area, text="Export to PDF", font=("Poppins", 10), command=self.export_to_pdf).place(x=930, y=730, width=120)

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

    def delete_selected_row(self):
        selected = self.test_table.selection()
        if not selected:
            messagebox.showwarning("No Selection", "Please select a row to delete.")
            return
        if messagebox.askyesno("Confirm", "Are you sure you want to delete the selected row?"):
            self.test_table.delete(selected[0])

    def edit_selected_row(self):
        # Optional: You can build a similar popup for editing if needed
        messagebox.showinfo("Edit", "Edit functionality not implemented yet.")

    def open_log_prompt(self):
        popup = tk.Toplevel(self)
        popup.title("Log Test Data")
        popup.configure(bg="white")
        popup.geometry("420x600")

        def make_entry(label_text):
            tk.Label(popup, text=label_text, font=("Poppins", 10), bg="white").pack(anchor="w", padx=30, pady=(5, 0))
            entry = tk.Entry(popup, font=("Poppins", 10), width=35)
            entry.pack(pady=5)
            return entry

        serial_entry = make_entry("Serial No.")
        name_entry = make_entry("Target Name")
        test_type_entry = make_entry("Test Type")
        target_pressure_entry = make_entry("Target Pressure (psi)")
        min_pressure_entry = make_entry("Min Pressure (psi)")
        max_pressure_entry = make_entry("Max Pressure (psi)")
        start_entry = make_entry("Start Time (HH:MM:SS)")
        end_entry = make_entry("End Time (HH:MM:SS)")
        notes_entry = make_entry("Notes (Optional)")

        def hms_to_seconds(hms_str):
            h, m, s = map(int, hms_str.split(":"))
            return h * 3600 + m * 60 + s

        def start_logging():
            try:
                serial = serial_entry.get().strip()
                name = name_entry.get().strip()
                target_p = target_pressure_entry.get().strip()
                test_type = test_type_entry.get().strip()
                min_p = min_pressure_entry.get().strip()
                max_p = max_pressure_entry.get().strip()
                start_t = start_entry.get().strip()
                end_t = end_entry.get().strip()
                notes = notes_entry.get().strip()

                if not (serial and name and target_p and min_p and max_p and start_t and end_t):
                    messagebox.showerror("Missing Info", "Please complete all required fields.")
                    return

                start_s = hms_to_seconds(start_t)
                end_s = hms_to_seconds(end_t)

                if end_s <= start_s:
                    messagebox.showerror("Invalid Range", "End time must be after start time.")
                    return

                duration = str(timedelta(seconds=(end_s - start_s)))
                date = datetime.now().strftime("%Y-%m-%d")

                row = (serial, name, test_type, date, duration, target_p, min_p, max_p, notes, start_s)
                tag = "row_even" if len(self.test_table.get_children()) % 2 == 0 else "row_odd"
                self.test_table.insert("", "end", values=row, tags=(tag,))
                popup.destroy()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to log data: {e}")

        tk.Button(popup, text="Submit", font=("Poppins", 10, "bold"), command=start_logging).pack(pady=20)

        popup.update_idletasks()
        popup.geometry(f"420x{popup.winfo_reqheight()}")  # Resize based on content
        popup.resizable(False, False)

    def export_to_csv(self):
        selected = self.test_table.selection()
        if not selected:
            messagebox.showwarning("No Selection", "Please select a row to export.")
            return

        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV Files", "*.csv")])
        if not file_path:
            return

        row = self.test_table.item(selected[0])['values']
        full_data = self.controller.get_chamber_data()

        start_seconds = int(row[9])
        # ✅ Convert 'HH:MM:SS' or 'H:MM:SS' duration to seconds
        h, m, s = map(int, row[4].split(":"))
        duration_seconds = h * 3600 + m * 60 + s
        end_seconds = start_seconds + duration_seconds

        filtered_data = [(t, p, temp) for t, p, temp in full_data if start_seconds <= t <= end_seconds]
        shifted_data = [(t - start_seconds, p, temp) for t, p, temp in filtered_data]

        with open(file_path, mode="w", newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["Test Info"])
            writer.writerow(self.test_table["columns"][:-1])
            writer.writerow(row[:-1])
            writer.writerow([])
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

        c = canvas.Canvas(file_path, pagesize=letter)
        width, height = letter
        c.setFont("Helvetica-Bold", 14)
        c.drawString(30, height - 50, "Test Report Export")
        y = height - 80

        headers = self.test_table["columns"][:-1]
        row = self.test_table.item(selected[0])['values']

        c.setFont("Helvetica-Bold", 10)
        for i, h in enumerate(headers):
            c.drawString(30 + i * 80, y, h)
        y -= 20
        c.setFont("Helvetica", 9)
        for i, val in enumerate(row[:-1]):
            c.drawString(30 + i * 80, y, str(val))

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

        full_data = self.controller.get_chamber_data()
        start_seconds = int(row[9])
        h, m, s = map(int, row[4].split(":"))
        duration_seconds = h * 3600 + m * 60 + s
        end_seconds = start_seconds + duration_seconds
        filtered_data = [(t, p, temp) for t, p, temp in full_data if start_seconds <= t <= end_seconds]
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
