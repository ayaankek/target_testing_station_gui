import tkinter as tk
from pages.side_menu import SideMenu  # ✅ already modularized

class LiveDataPage(tk.Frame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller

        self.window_width = 1440
        self.window_height = 900
        self.sidebar_width = int(0.2 * self.window_width)

        self.configure(bg="#D9D9D9")  # ✅ Same grey background
        self.place(width=self.window_width, height=self.window_height)

        # === Sidebar ===
        self.sidebar = SideMenu(self, controller=self.controller, active_page="Live Data")

        # === Content Area ===
        self.live_data_area = tk.Frame(
            self,
            bg="#D9D9D9",  # ✅ Same grey as dashboard area
            width=self.window_width - self.sidebar_width,
            height=self.window_height
        )
        self.live_data_area.place(x=self.sidebar_width, y=0)

        tk.Label(
            self.live_data_area,
            text="Live Data",
            font=("Poppins", 24, "bold"),
            bg="#D9D9D9"
        ).place(x=45, y=15)
