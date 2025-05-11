import tkinter as tk
from PIL import Image, ImageTk
from pathlib import Path
import requests
import time
from collections import deque
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import numpy as np
from tkinter import font
from pages.side_menu import SideMenu 

# === SystemMetrics ===
class SystemMetrics(tk.Canvas):
    def __init__(self, parent):
        parent_width = parent.winfo_reqwidth() or 1440
        parent_height = parent.winfo_reqheight() or 900

        width = int(0.47 * parent_width) + 30
        height = int(0.37 * parent_height)

        super().__init__(parent, width=width, height=height, bg="#D9D9D9", highlightthickness=0)
        self.width = width
        self.height = height
        self.assets_path = Path(__file__).resolve().parent.parent / "assets"

        user_icon = Image.open(self.assets_path / "hugeicons_gas-pipe.png").resize((40, 40))
        self.user_icon_img = ImageTk.PhotoImage(user_icon)

        check_icon = Image.open(self.assets_path / "StatusCheckIcon.png").resize((50, 50))
        self.check_icon_img = ImageTk.PhotoImage(check_icon)

        self.place(x=0, y=0)

    def embed_metrics_frame_dynamic(self, temperature, pressure):
        for widget in self.winfo_children():
            widget.destroy()

        frame = tk.Frame(self, bg='white', width=self.width, height=self.height)
        frame.place(x=0, y=0)

        tk.Label(frame, text="System Metrics", font=('Poppins', 16, 'bold'), bg='white').place(x=25, y=18)
        tk.Label(frame, image=self.user_icon_img, bg='white').place(x=self.width - 70, y=18)

        self.draw_metric(frame, f"{pressure:.0f} Psi", "#F58F8F", "#FFD3D3", pressure, 155, 30, 80)
        self.draw_metric(frame, f"{temperature:.0f} °C", "#5B93F5", "#A9D0FF", temperature, 50, 30, 150)

        tk.Label(frame, text="Leak Rate:", font=('Poppins', 14, 'bold'), bg='white').place(x=90, y=230)
        tk.Label(frame, text="2.1 x 10⁻⁹", font=('Poppins', 14, 'bold'), fg='green', bg='white').place(x=100, y=265)

        tk.Label(frame, text="Status:", font=('Poppins', 14, 'bold'), bg='white').place(x=310, y=230)
        tk.Label(frame, text="OK", font=('Poppins', 16, 'bold'), fg='green', bg='white').place(x=390, y=230)
        tk.Label(frame, image=self.check_icon_img, bg='white').place(x=self.width - 225, y=270)

    def draw_metric(self, parent, label_text, label_color, bar_color, value, max_value, x, y):
        label_width = 92
        bar_width = self.width - label_width - 61
        height = 50
        radius = 25

        filled_ratio = min(value / max_value, 1.0)
        filled_width = int(bar_width * filled_ratio)

        label = tk.Canvas(parent, width=label_width, height=height, bg='white', highlightthickness=0)
        label.place(x=x, y=y)
        label.create_rectangle(0, 0, label_width, height, fill=label_color, outline=label_color)
        label.create_text(label_width // 2, height // 2, text=label_text, fill="white", font=('Poppins', 10, 'bold'))

        tk.Frame(parent, width=1, height=height, bg="#C0C0C0").place(x=x + label_width, y=y)

        bar_canvas = tk.Canvas(parent, width=bar_width, height=height, bg='white', highlightthickness=0)
        bar_canvas.place(x=x + label_width + 1, y=y)

        self.draw_rounded_bar(bar_canvas, 0, 0, bar_width, height, "#EAEAEA", radius)
        if filled_width > 0:
            self.draw_rounded_bar(bar_canvas, 0, 0, filled_width, height, bar_color, radius if filled_width >= bar_width else 0)

    def draw_rounded_bar(self, canvas, x, y, width, height, color, round_right=25):
        canvas.create_rectangle(x, y, x + width - round_right, y + height, fill=color, outline=color)
        if round_right > 0:
            canvas.create_arc(x + width - 2 * round_right, y, x + width, y + height, start=270, extent=180, fill=color, outline=color)


class ValvesStatus(tk.Canvas):
    def __init__(self, parent):
        parent_width = parent.winfo_reqwidth() or 1440
        parent_height = parent.winfo_reqheight() or 900

        width = int(0.37 * parent_width)
        height = int(0.37 * parent_height)

        super().__init__(parent, width=width, height=height, bg="#D9D9D9", highlightthickness=0)
        self.width = width
        self.height = height

        self.assets_path = Path(__file__).resolve().parent.parent / "assets"

        shutoff_icon_path = self.assets_path / "ValveTabIcon.png"
        shutoff_icon = Image.open(shutoff_icon_path).resize((40, 40))
        self.shutoff_icon_img = ImageTk.PhotoImage(shutoff_icon)

        self.valve_states = {}
        self.valve_canvases = {}

        self.place(x=0, y=0)
        self.draw_rounded_tab()
        self.embed_valves_frame()


    def draw_rounded_tab(self):
        radius = 25
        self.create_round_rect(0, 0, self.width, self.height, radius, fill='white', outline='white')

    def embed_valves_frame(self):
        frame = tk.Frame(self, bg='white', width=self.width, height=self.height)
        frame.place(x=0, y=0)

        tk.Label(frame, text="Valves", font=('Poppins', 16, 'bold'), bg='white').place(x=20, y=18)
        tk.Label(frame, image=self.shutoff_icon_img, bg='white').place(x=self.width - 70, y=18)

        valves_grid = [
            ["He", "N₂", "Va", "Ve"],
            ["C-1", "C-2", "LD", "NV"],
            ["T-1", "T-2", "T-3", "T-4"],
        ]

        start_x = 35
        start_y = 90
        x_spacing = 100
        y_spacing = 80
        circle_size = 60

        for row_idx, row in enumerate(valves_grid):
            for col_idx, valve_name in enumerate(row):
                x = start_x + col_idx * x_spacing
                y = start_y + row_idx * y_spacing
                self.create_valve(frame, valve_name, x, y, circle_size)

    def create_valve(self, parent, valve_name, x, y, diameter):
        self.valve_states[valve_name] = "open"

        canvas = tk.Canvas(parent, width=diameter, height=diameter, bg='white', highlightthickness=0)
        canvas.place(x=x, y=y)

        self.draw_valve(canvas, valve_name, "green")
        canvas.bind("<Button-1>", lambda event, name=valve_name: self.toggle_valve(name))
        self.valve_canvases[valve_name] = canvas

    def draw_valve(self, canvas, valve_name, color_name):
        canvas.delete("all")
        color = "#5AD760" if color_name == "green" else "#D9D9D9"
        diameter = int(canvas['width'])
        canvas.create_oval(2, 2, diameter-2, diameter-2, fill=color, outline="white", width=2)
        canvas.create_text(diameter//2, diameter//2, text=valve_name, font=('Poppins', 10, 'bold'))

    def toggle_valve(self, valve_name):
        current_state = self.valve_states[valve_name]
        new_state = "closed" if current_state == "open" else "open"
        self.valve_states[valve_name] = new_state

        canvas = self.valve_canvases[valve_name]
        color = "green" if new_state == "open" else "gray"
        self.draw_valve(canvas, valve_name, color)

    def create_round_rect(self, x1, y1, x2, y2, r=25, **kwargs):
        self.create_arc(x1, y1, x1 + 2 * r, y1 + 2 * r, start=90, extent=90, **kwargs)
        self.create_arc(x2 - 2 * r, y1, x2, y1 + 2 * r, start=0, extent=90, **kwargs)
        self.create_arc(x2 - 2 * r, y2 - 2 * r, x2, y2, start=270, extent=90, **kwargs)
        self.create_arc(x1, y2 - 2 * r, x1 + 2 * r, y2, start=180, extent=90, **kwargs)
        self.create_rectangle(x1 + r, y1, x2 - r, y2, **kwargs)
        self.create_rectangle(x1, y1 + r, x2, y2 - r, **kwargs)

# === ChamberData ===
class ChamberData(tk.Canvas):
    def __init__(self, parent):
        parent_width = parent.winfo_reqwidth() or 1440
        parent_height = parent.winfo_reqheight() or 900

        width = int(0.6 * parent_width)
        height = int(0.45 * parent_height)

        super().__init__(parent, width=width, height=height, bg="#D9D9D9", highlightthickness=0)
        self.width = width
        self.height = height

        self.assets_path = Path(__file__).resolve().parent.parent / "assets"
        self.place(x=0, y=30)

    def update_graph(self, time_minutes, pressure_psi):
        # Keep only last 2 hours (120 minutes) of data
        recent_time = []
        recent_pressure = []
        for t, p in zip(time_minutes, pressure_psi):
            if time_minutes[-1] - t <= 120:
                recent_time.append(t)
                recent_pressure.append(p)

        for widget in self.winfo_children():
            widget.destroy()

        frame = tk.Frame(self, bg='white', width=self.width, height=self.height)
        frame.place(x=0, y=0)

        tk.Label(frame, text="Chamber Data", font=('Poppins', 16, 'bold'), bg='white').place(x=25, y=18)

        if getattr(self.master.master, "is_fallback", False):
             tk.Label(frame, text="⚠ Fallback Data Mode", font=('Poppins', 10), fg="red", bg='white').place(x=400, y=35)

        try:
            expand_icon = Image.open(self.assets_path / "ChamberDataIcon.png").resize((40, 40))
            self.expand_icon_img = ImageTk.PhotoImage(expand_icon)
            tk.Label(frame, image=self.expand_icon_img, bg='white').place(x=self.width - 70, y=18)
        except:
            pass

        fig, ax = plt.subplots(figsize=(6.2, 3))
        ax.plot(time_minutes, pressure_psi, marker='o', linestyle='-', color='blue')
        ax.set_xlabel('Time (mins)')
        ax.set_ylabel('Pressure (Psi)')
        ax.grid(True)
        fig.tight_layout()

        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.draw()
        canvas.get_tk_widget().place(x=20, y=60, width=self.width - 40, height=self.height - 80)

# === SystemStatus ===
class SystemStatus(tk.Canvas):
    def __init__(self, parent, chamber="Sealed", leak="Sealed", pump="Not Active"):
        super().__init__(parent, width=306, height=405, bg="white", highlightthickness=0)
        self.width = 306
        self.height = 405
        self.pack_propagate(False)
        self.configure(borderwidth=0)

        title_font = font.Font(family="Poppins", size=16, weight="bold")
        label_font = font.Font(family="Poppins", size=13)
        status_font = font.Font(family="Poppins", size=13, weight="bold")

        try:
            icon_path = Path(__file__).resolve().parent.parent / "assets" / "SystemStatusIcon.png"
            system_icon = Image.open(icon_path).resize((35, 35))
            self.system_icon_img = ImageTk.PhotoImage(system_icon)
        except:
            self.system_icon_img = None

        # Title
        title_frame = tk.Frame(self, bg="white")
        title_frame.pack(pady=(20, 10), fill="x", padx=20)

        tk.Label(title_frame, text="System Status", font=title_font, bg="white", fg="#333").pack(side="left")
        if self.system_icon_img:
            tk.Label(title_frame, image=self.system_icon_img, bg="white").pack(side="right")

        # Status rows
        def add_status_row(label, value, color):
            row = tk.Frame(self, bg="white")
            row.pack(anchor="w", padx=25, pady=5)
            tk.Label(row, text=f"{label}:", font=label_font, bg="white", fg="#222").pack(side="left")
            tk.Label(row, text=f"  {value}", font=status_font, bg="white", fg=color).pack(side="left")

        add_status_row("Chamber", chamber, "green" if chamber == "Sealed" else "red")
        add_status_row("Leak Detector", leak, "green" if leak == "Sealed" else "red")
        add_status_row("Pump", pump, "red" if pump == "Not Active" else "green")



class DashboardPage(tk.Frame):
    def __init__(self, master, controller, username="admin"):
        super().__init__(master)
        self.controller = controller
        self.username = username
        self.assets_path = Path(__file__).resolve().parent.parent / "assets"

        self.window_width = 1440
        self.window_height = 900
        self.sidebar_width = int(0.2 * self.window_width)

        self.selected_tab = "Dashboard"

        self.configure(bg="#D9D9D9")
        self.place(width=self.window_width, height=self.window_height)

        self.username = username
        self.create_sidebar()
        self.create_dashboard_area()

        self.time_data = deque(np.linspace(0, 150, 30), maxlen=30)
        self.pressure_data = deque(np.random.uniform(14, 16, 30), maxlen=30)
        self.start_time = time.time()

        self.is_fallback = True  # Always true with this version
        self.update_weather_data()


    def create_sidebar(self):
        sidebar = SideMenu(self, controller=self.controller, active_page="Dashboard", username=self.username)


    def create_sidebar_button(self, parent, text, icon_file, y, text_color="white", is_selected=False):
        try:
            icon = Image.open(self.assets_path / icon_file).resize((24, 24))
            icon_img = ImageTk.PhotoImage(icon)
            setattr(self, f"{text.lower().replace(' ', '_')}_icon", icon_img)
        except:
            icon_img = None

        container = tk.Frame(parent, bg="#005DAA", width=250, height=48)
        container.place(x=(self.sidebar_width - 170) // 2, y=y)

        if icon_img:
            tk.Label(container, image=icon_img, bg="#005DAA").pack(side="left", padx=(0, 30))
        tk.Label(container, text=text, fg=text_color, bg="#005DAA", font=('Poppins', 12, 'bold')).pack(side="left")


    def create_dashboard_area(self):
        self.dashboard_area = tk.Frame(self, bg="#D9D9D9", width=self.window_width - self.sidebar_width, height=self.window_height)
        self.dashboard_area.place(x=self.sidebar_width, y=0)

        tk.Label(self.dashboard_area, text="Dashboard", font=("Poppins", 24, "bold"), bg="#D9D9D9").place(x=45, y=15)

        self.chamber_data = ChamberData(self.dashboard_area)
        self.chamber_data.place(x=50, y=90)

        self.system_metrics = SystemMetrics(self.dashboard_area)
        self.system_metrics.place(x=50, y=self.window_height - self.system_metrics.height - 30)

        self.valves_status = ValvesStatus(self.dashboard_area)
        self.valves_status.place(x=675, y=self.window_height - self.system_metrics.height - 30)

        self.system_status = SystemStatus(self.dashboard_area)
        self.system_status.place(x=795, y=90)

        # === Username Display (Top Right) ===
        x_start = self.window_width - self.sidebar_width - 200
        y_pos = 20

        # Normal part
        tk.Label(
            self.dashboard_area,
            text="Logged in as:",
            font=("Poppins", 11),
            fg="#333",
            bg="#D9D9D9"
        ).place(x=x_start, y=y_pos)

        # Bold username part
        tk.Label(
            self.dashboard_area,
            text=self.username,
            font=("Poppins", 12, "bold"),
            fg="#333",
            bg="#D9D9D9"
        ).place(x=x_start + 110, y=y_pos - 1)  # minor alignment tweak


    def update_weather_data(self):
        from collections import deque
        import numpy as np

        self.time_data = deque(np.linspace(0, 150, 30), maxlen=30)
        self.pressure_data = deque(np.random.uniform(14.0, 16.0, 30), maxlen=30)
        temperature = 28
        pressure = 15

        print("🧪 Testing fallback")
        #print("Time data:", list(self.time_data))
        #print("Pressure data:", list(self.pressure_data))

        self.system_metrics.embed_metrics_frame_dynamic(temperature, pressure)
        self.chamber_data.update_graph(list(self.time_data), list(self.pressure_data))

        self.after(300000, self.update_weather_data)
