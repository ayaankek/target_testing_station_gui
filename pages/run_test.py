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

        # Sidebar
        self.sidebar = SideMenu(self, controller=self.controller, active_page="Run Test")

        # Header
        tk.Label(self.run_test_area, text="Run Test", font=("Poppins", 24, "bold"), bg="#D9D9D9").place(x=45, y=15)

        # Top-right user label
        x_start = self.window_width - self.sidebar_width - 200
        tk.Label(self.run_test_area, text="Logged in as:", font=("Poppins", 11), fg="#333", bg="#D9D9D9").place(x=x_start, y=20)
        tk.Label(self.run_test_area, text=self.username, font=("Poppins", 12, "bold"), fg="#333", bg="#D9D9D9").place(x=x_start + 110, y=19)

        # === Test Card Buttons ===
        card_width = 475
        card_height = 332
        card_y = 90
        spacing = 60

        # === PDD Test Card ===
        self.pdd_card = tk.Frame(self.run_test_area, width=card_width, height=card_height, bg="white", highlightbackground="#999", highlightthickness=1, cursor="hand2")
        self.pdd_card.place(x=45, y=card_y)
        tk.Label(self.pdd_card, text="PDD Test", font=("Poppins", 20, "bold"), bg="white", fg="#333").place(relx=0.5, rely=0.5, anchor="center")

        # === Gas Test Card ===
        self.gas_card = tk.Frame(self.run_test_area, width=card_width, height=card_height, bg="white", highlightbackground="#999", highlightthickness=1, cursor="hand2")
        self.gas_card.place(x=60 + card_width + spacing, y=card_y)
        tk.Label(self.gas_card, text="Gas Test", font=("Poppins", 20, "bold"), bg="white", fg="#333").place(relx=0.5, rely=0.5, anchor="center")

        # === Bind PDD Test Card Clicks ===
        self.pdd_card.bind("<Button-1>", lambda e: self.controller.show_pdd_test())
        for widget in self.pdd_card.winfo_children():
            widget.bind("<Button-1>", lambda e: self.controller.show_pdd_test())

        # === Bind Gas Test Card Clicks ===
        self.gas_card.bind("<Button-1>", lambda e: self.controller.show_gas_test())  # ✅ CHANGED
        for widget in self.gas_card.winfo_children():
            widget.bind("<Button-1>", lambda e: self.controller.show_gas_test())      # ✅ CHANGED


        # === Placeholder Graph ===
        graph_width = 1025
        graph_height = 400
        graph_x = 45
        graph_y = 470

        fig = Figure(figsize=(graph_width / 100, graph_height / 100), dpi=100)
        ax = fig.add_subplot(111)
        ax.plot([0, 1, 2, 3], [10, 15, 13, 18], marker='o')
        ax.set_title("Test Placeholder Plot")
        ax.set_xlabel("Time")
        ax.set_ylabel("Value")
        ax.grid(True)

        canvas = FigureCanvasTkAgg(fig, master=self.run_test_area)
        canvas.draw()
        canvas.get_tk_widget().place(x=graph_x, y=graph_y, width=graph_width, height=graph_height)
