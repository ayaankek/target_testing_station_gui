import tkinter as tk
from pathlib import Path
from PIL import Image, ImageTk

from pages.side_menu import SideMenu

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class RunTestPage(tk.Frame):
    def __init__(self, master, controller, username="admin"):
        super().__init__(master)
        self.controller = controller
        self.username = username

        self.window_width = 1440
        self.window_height = 900
        self.sidebar_width = int(0.2 * self.window_width)

        self.configure(bg="#D9D9D9")
        self.place(width=self.window_width, height=self.window_height)

        self.run_test_area = tk.Frame(self, bg="#D9D9D9", width=self.window_width - self.sidebar_width, height=self.window_height)
        self.run_test_area.place(x=self.sidebar_width, y=0)

        self.sidebar = SideMenu(self, controller=self.controller, active_page="Run Test")

        # Header
        tk.Label(self.run_test_area, text="Run Test", font=("Poppins", 24, "bold"), bg="#D9D9D9").place(x=45, y=15)
        
        # Top-right user label
        x_start = self.window_width - self.sidebar_width - 200
        tk.Label(self.run_test_area, text="Logged in as:", font=("Poppins", 11), fg="#333", bg="#D9D9D9").place(x=x_start, y=20)
        tk.Label(self.run_test_area, text=self.username, font=("Poppins", 12, "bold"), fg="#333", bg="#D9D9D9").place(x=x_start + 110, y=19)

        # === Test Buttons ===
        button_width = 475
        button_height = 332
        button_y = 90
        spacing = 60

        pdd_button = tk.Frame(self.run_test_area, width=button_width, height=button_height, bg="white", highlightthickness=0)
        pdd_button.place(x=45, y=button_y)
        tk.Label(pdd_button, text="PDD Test", font=("Poppins", 20, "bold"), bg="white", fg="#333").place(relx=0.5, rely=0.5, anchor="center")

        gas_button = tk.Frame(self.run_test_area, width=button_width, height=button_height, bg="white", highlightthickness=0)
        gas_button.place(x=60 + button_width + spacing, y=button_y)
        tk.Label(gas_button, text="Gas Test", font=("Poppins", 20, "bold"), bg="white", fg="#333").place(relx=0.5, rely=0.5, anchor="center")

        # === Bind click handlers AFTER widgets are created ===
        pdd_button.bind("<Button-1>", lambda e: print("🧪 PDD Test clicked"))
        gas_button.bind("<Button-1>", lambda e: print("🧪 Gas Test clicked"))

        # === Placeholder Graph ===
        graph_width = 1025
        graph_height = 400
        graph_x = 45
        graph_y = 470  

        # Create a basic plot
        fig = Figure(figsize=(graph_width / 100, graph_height / 100), dpi=100)
        ax = fig.add_subplot(111)
        ax.plot([0, 1, 2, 3], [10, 15, 13, 18], marker='o')  # dummy data
        ax.set_title("Test Placeholder Plot")
        ax.set_xlabel("Time")
        ax.set_ylabel("Value")
        ax.grid(True)

        # Embed it into the GUI
        canvas = FigureCanvasTkAgg(fig, master=self.run_test_area)
        canvas.draw()
        canvas.get_tk_widget().place(x=graph_x, y=graph_y, width=graph_width, height=graph_height)


