import tkinter as tk
from PIL import Image, ImageTk
from pathlib import Path
import numpy as np
from collections import deque

from pages.side_menu import SideMenu
from pages.dashboard import ChamberData
from utils.weather import get_weather_data

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt


class TargetChamber(tk.Canvas):
    def __init__(self, parent):
        width = 306
        height = 405
        super().__init__(parent, width=width, height=height, bg="#D9D9D9", highlightthickness=0)
        self.width = width
        self.height = height
        self.assets_path = Path(__file__).resolve().parent.parent / "assets"

        self.icon_img = None
        try:
            icon = Image.open(self.assets_path / "hugeicons_gas-pipe.png").resize((35, 35))
            self.icon_img = ImageTk.PhotoImage(icon)
        except:
            pass

        self.embed_vertical_metrics(temperature=28, pressure=15)  # Placeholder until updated

    def embed_vertical_metrics(self, temperature, pressure):
        for widget in self.winfo_children():
            widget.destroy()

        frame = tk.Frame(self, bg="white", width=self.width, height=self.height)
        frame.place(x=0, y=0)

        # === Title and Icon ===
        tk.Label(frame, text="Target Chamber", font=('Poppins', 16, 'bold'), bg="white").place(x=20, y=20)
        if self.icon_img:
            tk.Label(frame, image=self.icon_img, bg="white").place(x=self.width - 50, y=20)

        # === Updated Bar Dimensions ===
        bar_width = 80
        bar_height = 210
        label_height = 58
        spacing = 30
        total_width = 2 * bar_width + spacing
        total_height = bar_height + label_height + 10

        start_x = (self.width - total_width) // 2
        start_y = (self.height - total_height) // 2 + 30  # vertically center below title

        self.draw_vertical_metric(frame, f"{pressure:.0f} Pa", "#F58F8F", "#FFD3D3", pressure, 155, x=start_x, y=start_y, bar_width=bar_width, bar_height=bar_height)
        self.draw_vertical_metric(frame, f"{temperature:.0f} °C", "#5B93F5", "#A9D0FF", temperature, 50, x=start_x + bar_width + spacing, y=start_y, bar_width=bar_width, bar_height=bar_height)


    def draw_vertical_metric(self, parent, label_text, label_color, bar_color, value, max_value, x, y, bar_width=60, bar_height=200):
        bar_width = 80
        bar_height = 210
        label_height = 58
        radius = 30

        filled_ratio = min(value / max_value, 1.0)
        filled_height = int(bar_height * filled_ratio)

        # === Label below the bar ===
        label_canvas = tk.Canvas(parent, width=bar_width, height=label_height, bg="white", highlightthickness=0)
        label_canvas.place(x=x, y=y + bar_height)
        label_canvas.create_rectangle(0, 0, bar_width, label_height, fill=label_color, outline=label_color)
        label_canvas.create_text(bar_width // 2, label_height // 2, text=label_text, fill="white", font=('Poppins', 12, 'bold'))

        # === Bar Background with rounded top ===
        bar_canvas = tk.Canvas(parent, width=bar_width, height=bar_height, bg="white", highlightthickness=0)
        bar_canvas.place(x=x, y=y)
        bar_canvas.create_rectangle(0, radius, bar_width, bar_height, fill="#EAEAEA", outline="#EAEAEA")
        bar_canvas.create_arc(0, 0, bar_width, 2 * radius, start=0, extent=180, fill="#EAEAEA", outline="#EAEAEA")

        # === Filled section (bottom-up) ===
        if filled_height > 0:
            y_fill = bar_height - filled_height

            # Draw filled bar body only — FLAT top (no arc)
            bar_canvas.create_rectangle(
                0, y_fill, bar_width, bar_height,
                fill=bar_color, outline=bar_color
            )


    def animate_bar(self, parent, label, value_text, value, max_value, x, y, color, fill):
        tk.Label(parent, text=label, font=('Poppins', 12, 'bold'), bg='white').place(x=x + 35, y=y)
        tk.Label(parent, text=value_text, font=('Poppins', 11), bg='white').place(x=x + 20, y=y + 190)

        bar_frame = tk.Frame(parent, width=60, height=150, bg="#EAEAEA")
        bar_frame.place(x=x + 10, y=y + 30)

        canvas = tk.Canvas(bar_frame, width=60, height=150, bg="#EAEAEA", highlightthickness=0)
        canvas.pack()

        target_height = int((min(value / max_value, 1.0)) * 150)
        self.animate_fill(canvas, 60, 150, target_height, fill)

    def animate_fill(self, canvas, width, full_height, target_height, color):
        def step(current_height):
            canvas.delete("all")
            canvas.create_rectangle(0, full_height - current_height, width, full_height, fill=color, outline="")
            if current_height < target_height:
                self.after(20, step, current_height + 5)
        step(0)

class LiveDataPage(tk.Frame):
    def __init__(self, master, controller, username="admin"):
        super().__init__(master)
        self.controller = controller
        self.username = username

        self.window_width = 1440
        self.window_height = 900
        self.sidebar_width = int(0.2 * self.window_width)

        self.configure(bg="#D9D9D9")
        self.place(width=self.window_width, height=self.window_height)

        self.live_data_area = tk.Frame(self, bg="#D9D9D9", width=self.window_width - self.sidebar_width, height=self.window_height)
        self.live_data_area.place(x=self.sidebar_width, y=0)

        self.sidebar = SideMenu(self, controller=self.controller, active_page="Live Data")

        self.chamber_data = ChamberData(self.live_data_area)
        self.chamber_data.place(x=50, y=90)

        self.target_chamber = TargetChamber(self.live_data_area)
        self.target_chamber.place(x=795, y=90)

        self.leak_test = LeakTest(self.live_data_area)
        self.leak_test.place(x=50, y=self.window_height - 333 - 25)  # 50 px margin from bottom

        self.rate_fall_test = RateOfFallTest(self.live_data_area)
        self.rate_fall_test.place(x=602, y=self.window_height - 333 - 25)

        # Simulated data
        leak_time = deque(np.linspace(0, 120, 15), maxlen=15)
        leak_pressure = deque(np.random.uniform(10, 90, 15), maxlen=15)
        self.leak_test.update_graph(list(leak_time), list(leak_pressure))

        fall_time = deque(np.linspace(0, 120, 15), maxlen=15)
        fall_pressure = deque(np.random.uniform(10, 90, 15), maxlen=15)
        self.rate_fall_test.update_graph(list(fall_time), list(fall_pressure))

        tk.Label(self.live_data_area, text="Live Data", font=("Poppins", 24, "bold"), bg="#D9D9D9").place(x=45, y=15)

        x_start = self.window_width - self.sidebar_width - 200
        y_pos = 20
        tk.Label(self.live_data_area, text="Logged in as:", font=("Poppins", 11), fg="#333", bg="#D9D9D9").place(x=x_start, y=y_pos)
        tk.Label(self.live_data_area, text=self.username, font=("Poppins", 12, "bold"), fg="#333", bg="#D9D9D9").place(x=x_start + 110, y=y_pos - 1)

        self.time_data = deque(np.linspace(0, 150, 30), maxlen=30)
        self.pressure_data = deque(np.random.uniform(14, 16, 30), maxlen=30)

        self.update_live_data()

    def update_live_data(self):
        temperature, pressure = get_weather_data()

        # Update graph
        self.pressure_data.append(pressure)
        self.time_data.append(self.time_data[-1] + 5)
        self.chamber_data.update_graph(list(self.time_data), list(self.pressure_data))

        # Update target chamber
        self.target_chamber.embed_vertical_metrics(temperature, pressure)

        self.after(60000, self.update_live_data)  # refresh every 60 seconds

class LeakTest(tk.Canvas):
    def __init__(self, parent):
        width = 500
        height = 333
        super().__init__(parent, width=width, height=height, bg="#D9D9D9", highlightthickness=0)
        self.width = width
        self.height = height
        self.assets_path = Path(__file__).resolve().parent.parent / "assets"
        self.place(x=0, y=0)

    def update_graph(self, time_data, pressure_data):
        for widget in self.winfo_children():
            widget.destroy()

        frame = tk.Frame(self, bg='white', width=self.width, height=self.height)
        frame.place(x=0, y=0)

        tk.Label(frame, text="Leak Test", font=('Poppins', 16, 'bold'), bg='white').place(x=25, y=18)

        try:
            expand_icon = Image.open(self.assets_path / "ChamberDataIcon.png").resize((40, 40))
            self.expand_icon_img = ImageTk.PhotoImage(expand_icon)
            tk.Label(frame, image=self.expand_icon_img, bg='white').place(x=self.width - 60, y=20)
        except:
            pass

        fig, ax = plt.subplots(figsize=(5.8, 2.8))
        ax.plot(time_data, pressure_data, color='blue', marker='o')
        ax.set_xlabel('Time (mins)')
        ax.set_ylabel('Pressure (Psi)')
        ax.grid(True)
        fig.tight_layout()

        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.draw()
        plt.close(fig)  # Prevents backend conflicts
        canvas.get_tk_widget().place(x=20, y=60, width=self.width - 40, height=self.height - 80)

class RateOfFallTest(tk.Canvas):
    def __init__(self, parent):
        width = 500
        height = 333
        super().__init__(parent, width=width, height=height, bg="#D9D9D9", highlightthickness=0)
        self.width = width
        self.height = height
        self.assets_path = Path(__file__).resolve().parent.parent / "assets"
        self.place(x=0, y=0)

    def update_graph(self, time_data, pressure_data):
        for widget in self.winfo_children():
            widget.destroy()

        frame = tk.Frame(self, bg='white', width=self.width, height=self.height)
        frame.place(x=0, y=0)

        tk.Label(frame, text="Rate of Fall Test", font=('Poppins', 16, 'bold'), bg='white').place(x=25, y=18)

        try:
            expand_icon = Image.open(self.assets_path / "ChamberDataIcon.png").resize((40, 40))
            self.expand_icon_img = ImageTk.PhotoImage(expand_icon)
            tk.Label(frame, image=self.expand_icon_img, bg='white').place(x=self.width - 60, y=20)
        except:
            pass

        fig, ax = plt.subplots(figsize=(5.8, 2.8))
        ax.plot(time_data, pressure_data, color='blue', marker='o')
        ax.set_xlabel('Time (mins)')
        ax.set_ylabel('Pressure (Psi)')
        ax.grid(True)
        fig.tight_layout()

        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.draw()
        canvas.get_tk_widget().place(x=20, y=60, width=self.width - 40, height=self.height - 80)

