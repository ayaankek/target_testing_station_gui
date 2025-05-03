import tkinter as tk
from pages.side_menu import SideMenu
from pages.dashboard import ChamberData
from collections import deque
import numpy as np

class LiveDataPage(tk.Frame):
    def __init__(self, master, controller, username="Guest"):
        super().__init__(master)
        self.controller = controller
        self.username = username

        self.window_width = 1440
        self.window_height = 900
        self.sidebar_width = int(0.2 * self.window_width)

        self.configure(bg="#D9D9D9")
        self.place(width=self.window_width, height=self.window_height)

        # === Content Area ===
        self.live_data_area = tk.Frame(
            self,
            bg="#D9D9D9",
            width=self.window_width - self.sidebar_width,
            height=self.window_height
        )
        self.live_data_area.place(x=self.sidebar_width, y=0)

        # === Sidebar ===
        self.sidebar = SideMenu(self, controller=self.controller, active_page="Live Data")

        # === Chamber Data Graph ===
        self.chamber_data = ChamberData(self.live_data_area)
        self.chamber_data.place(x=50, y=90)

        # Simulated pressure data
        time_data = deque(np.linspace(0, 150, 30), maxlen=30)
        pressure_data = deque(np.random.uniform(14, 16, 30), maxlen=30)

        try:
            self.chamber_data.update_graph(list(time_data), list(pressure_data))
            print("✅ update_graph ran successfully.")
        except Exception as e:
            print("🔥 update_graph failed:", e)


        # === Header
        tk.Label(
            self.live_data_area,
            text="Live Data",
            font=("Poppins", 24, "bold"),
            bg="#D9D9D9"
        ).place(x=45, y=15)

        # === Username Display (Top Right) ===
        x_start = self.window_width - self.sidebar_width - 200
        y_pos = 20

        # Normal part
        tk.Label(
            self.live_data_area,
            text="Logged in as:",
            font=("Poppins", 11),
            fg="#333",
            bg="#D9D9D9"
        ).place(x=x_start, y=y_pos)

        # Bold username part
        tk.Label(
            self.live_data_area,
            text=self.username,
            font=("Poppins", 12, "bold"),
            fg="#333",
            bg="#D9D9D9"
        ).place(x=x_start + 110, y=y_pos - 1)  # slight vertical alignment

       
