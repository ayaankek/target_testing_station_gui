import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from pages.side_menu import SideMenu

class GasTestPage(tk.Frame):
    def __init__(self, master, controller=None, username="admin"):
        super().__init__(master, bg="#D9D9D9")
        self.controller = controller
        self.username = username
        self.test_running = False  # ✅ Test state flag

        self.window_width = 1440
        self.window_height = 900
        self.sidebar_width = int(0.2 * self.window_width)

        # === Sidebar ===
        self.sidebar = SideMenu(self, controller=self.controller, active_page="Run Test")
        self.sidebar.place(x=0, y=0)

        # === Main content area ===
        self.test_area = tk.Frame(self, bg="#D9D9D9", width=self.window_width - self.sidebar_width, height=self.window_height)
        self.test_area.place(x=self.sidebar_width, y=0)

        # === Page Title ===
        tk.Label(
            self.test_area,
            text="Run Test – Gas",
            font=("Poppins", 24, "bold"),
            bg="#D9D9D9",
            fg="#222"
        ).place(x=30, y=15)

        # ✅ Toggle Button (Start/Stop)
        self.test_button = tk.Button(
            self.test_area,
            text="▶ Start Test",
            font=("Poppins", 10, "bold"),
            bg="#4CAF50",  # Green
            fg="white",
            relief="flat",
            command=self.toggle_test
        )
        self.test_button.place(x=325, y=25, width=110, height=30)

        # === Top-right user label ===
        x_start = self.window_width - self.sidebar_width - 200
        tk.Label(self.test_area, text="Logged in as:", font=("Poppins", 11), fg="#333", bg="#D9D9D9").place(x=x_start, y=20)
        tk.Label(self.test_area, text=self.username, font=("Poppins", 12, "bold"), fg="#333", bg="#D9D9D9").place(x=x_start + 110, y=19)

        # === Sample Data ===
        self.time_data = [0, 15, 30, 45, 60, 75, 90, 105, 120]
        self.pressure_data = [20, 35, 45, 30, 50, 65, 60, 75, 85]

        # === Graph Cards ===
        self.create_graph_card(
            parent=self.test_area,
            x=30,
            y=105,
            title="Leak Test",
            data_x=self.time_data,
            data_y=self.pressure_data
        )

        self.create_graph_card(
            parent=self.test_area,
            x=30,
            y=500,
            title="Rate of Fall Test",
            data_x=self.time_data,
            data_y=[p - 10 for p in self.pressure_data]
        )

    def toggle_test(self):
        self.test_running = not self.test_running
        if self.test_running:
            self.test_button.config(
                text="⏹ Stop Test",
                bg="#F44336"  # Red
            )
            print("✅ Gas test started")
        else:
            self.test_button.config(
                text="▶ Start Test",
                bg="#4CAF50"  # Green
            )
            print("⏹️ Gas test stopped")

    def create_graph_card(self, parent, x, y, title, data_x, data_y):
        card_width = 529
        card_height = 333

        card = tk.Frame(parent, width=card_width, height=card_height, bg="white", highlightthickness=1, highlightbackground="#ccc")
        card.place(x=x, y=y)

        tk.Label(card, text=title, font=("Poppins", 14, "bold"), bg="white", anchor="w").place(x=20, y=10)

        fig = Figure(figsize=(5.0, 2.5), dpi=100)
        ax = fig.add_subplot(111)
        ax.plot(data_x, data_y, marker='o', markersize=4, linewidth=2, color="#009944")
        ax.set_xlabel("Time (mins)", fontsize=9)
        ax.set_ylabel("Pressure (Psi)", fontsize=9)
        ax.tick_params(labelsize=8)
        ax.grid(True)
        fig.subplots_adjust(left=0.15, right=0.95, top=0.88, bottom=0.2)

        canvas = FigureCanvasTkAgg(fig, master=card)
        canvas.draw()
        canvas.get_tk_widget().place(x=15, y=40, width=500, height=280)
