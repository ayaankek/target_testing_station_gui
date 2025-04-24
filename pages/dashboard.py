import tkinter as tk
from tkinter import ttk
from pathlib import Path

class DashboardPage(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg="#F0F0F0")

        self.place(relwidth=1, relheight=1)
        canvas = tk.Canvas(self, bg="#F0F0F0", height=900, width=1440, bd=0, highlightthickness=0)
        canvas.place(x=0, y=0)

        # Sidebar
        canvas.create_rectangle(0, 0, 280, 900, fill="#005DAB", outline="")
        canvas.create_rectangle(0, 270, 294, 867, fill="#000000", outline="")
        canvas.create_rectangle(55, 42, 225, 212, fill="#FFFFFF", outline="")
        canvas.create_text(344, 42, anchor="nw", text="Dashboard", fill="#353535", font=("Segoe UI", 36, "bold"))

        layout = {
            "chamber_data": (343, 102, 328, 240),
            "system_status": (720, 102, 656, 325),
            "system_metrics": (342, 366, 328, 240),
            "valves": (344, 630, 328, 240),
            "chart_area": (720, 486, 656, 350),
        }

        # Chamber Data
        x, y, w, h = layout["chamber_data"]
        chamber = tk.Frame(self, bg="white")
        chamber.place(x=x, y=y, width=w, height=h)
        tk.Label(chamber, text="Chamber Data", font=("Segoe UI", 14, "bold"), bg="white").pack(pady=10)

        # System Status
        x, y, w, h = layout["system_status"]
        status = tk.Frame(self, bg="white")
        status.place(x=x, y=y, width=w, height=h)
        tk.Label(status, text="System Status", font=("Segoe UI", 14, "bold"), bg="white").pack(pady=10)
        for label, value, color in [
            ("Chamber:", "Sealed", "green"),
            ("Leak Detector:", "Sealed", "green"),
            ("Pump:", "Not Active", "red"),
        ]:
            row = tk.Frame(status, bg="white")
            row.pack(anchor="w", padx=20, pady=5)
            tk.Label(row, text=label, font=("Segoe UI", 11), bg="white").pack(side="left")
            tk.Label(row, text=value, font=("Segoe UI", 11, "bold"), fg=color, bg="white").pack(side="left")

        # System Metrics
        x, y, w, h = layout["system_metrics"]
        metrics = tk.Frame(self, bg="white")
        metrics.place(x=x, y=y, width=w, height=h)
        tk.Label(metrics, text="System Metrics", font=("Segoe UI", 14, "bold"), bg="white").pack(pady=10)
        for val in ["110 PSI", "27°C"]:
            row = tk.Frame(metrics, bg="white")
            row.pack(anchor="w", padx=20, pady=5)
            tk.Label(row, text=val, font=("Segoe UI", 11), bg="white").pack(side="left")
            ttk.Progressbar(row, length=180).pack(side="left", padx=10)
        tk.Label(metrics, text="Leak Rate: 2.1x10⁶", bg="white").pack(pady=5)
        tk.Label(metrics, text="Status: OK", fg="green", bg="white", font=("Segoe UI", 11, "bold")).pack()

        # Valves
        x, y, w, h = layout["valves"]
        valves = tk.Frame(self, bg="white")
        valves.place(x=x, y=y, width=w, height=h)
        tk.Label(valves, text="Valves", font=("Segoe UI", 14, "bold"), bg="white").pack(pady=10)
        grid = tk.Frame(valves, bg="white")
        grid.pack()
        valve_names = ["He", "N2", "Vo", "W", "C1", "C2", "T1", "T2", "T3", "T4"]
        for i, name in enumerate(valve_names):
            color = "green" if "T" not in name else "gray"
            tk.Button(grid, text=name, bg=color, fg="white", width=4).grid(row=i//5, column=i%5, padx=5, pady=5)

        # Chart Area
        x, y, w, h = layout["chart_area"]
        chart = tk.Frame(self, bg="white")
        chart.place(x=x, y=y, width=w, height=h)
        tk.Label(chart, text="(Chart/Graph Placeholder)", font=("Segoe UI", 14), bg="white").pack(pady=20)
