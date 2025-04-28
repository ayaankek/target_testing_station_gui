import tkinter as tk
from PIL import Image, ImageTk
from pathlib import Path

# === System Metrics Card ===
import tkinter as tk
from PIL import Image, ImageTk
from pathlib import Path

# === System Metrics Card ===
class SystemMetrics(tk.Canvas):
    def __init__(self, parent):
        parent_width = parent.winfo_reqwidth() or 1440
        parent_height = parent.winfo_reqheight() or 900

        width = int(0.47 * parent_width) + 30  # Expand by 30px
        height = int(0.37 * parent_height)

        super().__init__(parent, width=width, height=height, bg="#D9D9D9", highlightthickness=0)
        self.width = width
        self.height = height

        self.assets_path = Path(__file__).resolve().parent.parent / "assets"

        user_icon_path = self.assets_path / "hugeicons_gas-pipe.png"
        user_icon = Image.open(user_icon_path).resize((40, 40))
        self.user_icon_img = ImageTk.PhotoImage(user_icon)

        check_icon_path = self.assets_path / "StatusCheckIcon.png"
        check_icon = Image.open(check_icon_path).resize((42, 42))
        self.check_icon_img = ImageTk.PhotoImage(check_icon)

        self.place(x=0, y=0)
        self.draw_rounded_tab()
        self.embed_metrics_frame()

    def draw_rounded_tab(self):
        radius = 25
        self.create_round_rect(0, 0, self.width, self.height, radius, fill='white', outline='white')

    def embed_metrics_frame(self):
        frame = tk.Frame(self, bg='white', width=self.width, height=self.height)
        frame.place(x=0, y=0)

        pressure = 110
        temperature = 27

        # Header
        tk.Label(frame, text="System Metrics", font=('Poppins', 16, 'bold'), bg='white').place(x=25, y=18)
        tk.Label(frame, image=self.user_icon_img, bg='white').place(x=self.width - 70, y=18)

        self.draw_metric(frame, "110 Psi", "#F58F8F", "#FFD3D3", pressure, 155, 30, 80)
        self.draw_metric(frame, "27 °C", "#5B93F5", "#A9D0FF", temperature, 50, 30, 150)

        # Leak Rate and Status
        tk.Label(frame, text="Leak Rate:", font=('Poppins', 14, 'bold'), bg='white').place(x=90, y=230)
        tk.Label(frame, text="2.1 x 10⁻⁹", font=('Poppins', 14, 'bold'), fg='green', bg='white').place(x=100, y=265)

        tk.Label(frame, text="Status:", font=('Poppins', 14, 'bold'), bg='white').place(x=310, y=230)
        tk.Label(frame, text="OK", font=('Poppins', 16, 'bold'), fg='green', bg='white').place(x=390, y=230)

        tk.Label(frame, image=self.check_icon_img, bg='white').place(x=self.width - 100, y=270)

    def draw_metric(self, parent, label_text, label_color, bar_color, value, max_value, x, y):
        label_width = 92
        bar_width = self.width - label_width - 61  # Adjusted
        height = 50
        radius = 25

        filled_ratio = value / max_value
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
            self.draw_rounded_bar(bar_canvas, 0, 0, filled_width, height, bar_color,
                                  radius if filled_width >= bar_width else 0)

    def draw_rounded_bar(self, canvas, x, y, width, height, color, round_right=25):
        canvas.create_rectangle(x, y, x + width - round_right, y + height, fill=color, outline=color)
        if round_right > 0:
            canvas.create_arc(x + width - 2 * round_right, y, x + width, y + height,
                              start=270, extent=180, fill=color, outline=color)

    def create_round_rect(self, x1, y1, x2, y2, r=25, **kwargs):
        self.create_arc(x1, y1, x1 + 2 * r, y1 + 2 * r, start=90, extent=90, **kwargs)
        self.create_arc(x2 - 2 * r, y1, x2, y1 + 2 * r, start=0, extent=90, **kwargs)
        self.create_arc(x2 - 2 * r, y2 - 2 * r, x2, y2, start=270, extent=90, **kwargs)
        self.create_arc(x1, y2 - 2 * r, x1 + 2 * r, y2, start=180, extent=90, **kwargs)
        self.create_rectangle(x1 + r, y1, x2 - r, y2, **kwargs)
        self.create_rectangle(x1, y1 + r, x2, y2 - r, **kwargs)


# === Valves Status Section ===
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

# === Dashboard Page ===
class DashboardPage(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.assets_path = Path(__file__).resolve().parent.parent / "assets"

        self.window_width = 1440
        self.window_height = 900
        self.sidebar_width = int(0.2 * self.window_width)

        self.configure(bg="#D9D9D9")
        self.place(width=self.window_width, height=self.window_height)

        self.create_sidebar()
        self.create_dashboard_area()

    def create_sidebar(self):
        sidebar = tk.Frame(self, bg="#005DAA", width=self.sidebar_width, height=self.window_height)
        sidebar.place(x=0, y=0)

        try:
            logo = Image.open(self.assets_path / "LLNL Logo Circle.png").resize((170, 170))
            self.logo_img = ImageTk.PhotoImage(logo)
            tk.Label(sidebar, image=self.logo_img, bg="#005DAA").place(x=(self.sidebar_width - 170) // 2, y=30)
        except:
            tk.Label(sidebar, text="LLNL", bg="#005DAA", fg="white", font=('Poppins', 16)).place(x=20, y=40)

        buttons = [
            ("Dashboard", "Selected Dashboard Button Icon.png"),
            ("Live Data", "Live Data Button Icon.png"),
            ("Run Test", "Run Test Button Icon.png"),
            ("Reports", "Reports Button Icon.png"),
            ("Layout", "Layout Button Icon.png"),
            ("Settings", "Settings Button Icon.png"),
            ("Logout", "Logout Button Icon.png"),
        ]

        base_y = 285
        spacing = 72

        for i, (text, icon_file) in enumerate(buttons):
            if text == "Settings":
                base_y += 150 - spacing

            self.create_sidebar_button(sidebar, text, icon_file, base_y + i * spacing)

    def create_sidebar_button(self, parent, text, icon_file, y):
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
        tk.Label(container, text=text, fg="white", bg="#005DAA", font=('Poppins', 12, 'bold')).pack(side="left")

    def create_dashboard_area(self):
        dashboard_area = tk.Frame(self, bg="#D9D9D9", width=self.window_width - self.sidebar_width, height=self.window_height)
        dashboard_area.place(x=self.sidebar_width, y=0)

        self.system_metrics = SystemMetrics(dashboard_area)
        metrics_width = self.system_metrics.width
        metrics_height = self.system_metrics.height
        self.system_metrics.place(x=50, y=self.window_height - metrics_height - 50)

        self.valves_status = ValvesStatus(dashboard_area)
        self.valves_status.place(x=675, y=self.window_height - metrics_height - 50)
