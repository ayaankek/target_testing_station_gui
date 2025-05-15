import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from pages.side_menu import SideMenu


class PDDTestPage(tk.Frame):
    def __init__(self, master, controller=None, username="admin"):
        super().__init__(master, bg="#D9D9D9")
        self.controller = controller
        self.username = username

        self.window_width = 1440
        self.window_height = 900
        self.sidebar_width = int(0.2 * self.window_width)

        # === Sidebar ===
        self.sidebar = SideMenu(self, controller=master.master, active_page="Run Test")
        self.sidebar.place(x=0, y=0)

        # === Main content area ===
        self.test_area = tk.Frame(self, bg="#D9D9D9", width=self.window_width - self.sidebar_width, height=self.window_height)
        self.test_area.place(x=self.sidebar_width, y=0)

        # === Page Title ===
        tk.Label(
            self.test_area,
            text="Run Test – PDD",
            font=("Poppins", 24, "bold"),
            bg="#D9D9D9",
            fg="#222"
        ).place(x=30, y=15)

        # === Top-right user label ===
        x_start = self.window_width - self.sidebar_width - 200
        tk.Label(self.test_area, text="Logged in as:", font=("Poppins", 11), fg="#333", bg="#D9D9D9").place(x=x_start, y=20)
        tk.Label(self.test_area, text=self.username, font=("Poppins", 12, "bold"), fg="#333", bg="#D9D9D9").place(x=x_start + 110, y=19)


        # === Generate fallback data ===
        self.time_data = [0, 15, 30, 45, 60, 75, 90, 105, 120]
        self.pressure_data = [15, 20, 45, 70, 40, 60, 85, 65, 90]

        # === Create Leak Test Graph ===
        self.create_graph_card(
            parent=self.test_area,
            x=30,
            y=105,
            title="Leak Test",
            data_x=self.time_data,
            data_y=self.pressure_data
        )

        # === Create Rate of Fall Test Graph ===
        self.create_graph_card(
            parent=self.test_area,
            x=30,
            y=500,
            title="Rate of Fall Test",
            data_x=self.time_data,
            data_y=self.pressure_data  # or other fallback data if desired
        )

    def create_graph_card(self, parent, x, y, title, data_x, data_y):
        card_width = 529
        card_height = 333

        # === Outer card container (Frame instead of Canvas for layout stability)
        card = tk.Frame(parent, width=card_width, height=card_height, bg="white", highlightthickness=1, highlightbackground="#ccc")
        card.place(x=x, y=y)

        # === Title
        title_label = tk.Label(card, text=title, font=("Poppins", 14, "bold"), bg="white", anchor="w")
        title_label.place(x=20, y=10)

        # === Graph
        fig = Figure(figsize=(5.0, 2.5), dpi=100)
        ax = fig.add_subplot(111)
        ax.plot(data_x, data_y, marker='o', markersize=4, linewidth=2, color="#FF3B3B")
        ax.set_xlabel("Time (mins)", fontsize=9)
        ax.set_ylabel("Pressure (Psi)", fontsize=9)
        ax.tick_params(labelsize=8)
        ax.grid(True)
        fig.subplots_adjust(left=0.15, right=0.95, top=0.88, bottom=0.2)

        canvas = FigureCanvasTkAgg(fig, master=card)
        canvas.draw()
        canvas.get_tk_widget().place(x=15, y=40, width=500, height=280)




