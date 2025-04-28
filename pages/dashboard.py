import tkinter as tk
from PIL import Image, ImageTk
from pathlib import Path

class SystemMetrics(tk.Canvas):
    def __init__(self, parent):
        super().__init__(parent, width=538, height=336, bg="#D9D9D9", highlightthickness=0)
        self.place(x=0, y=0)
        self.draw_rounded_tab()
        self.embed_metrics_frame()

    def draw_rounded_tab(self):
        radius = 25
        self.create_round_rect(0, 0, 538, 336, radius, fill='white', outline='white')

    def embed_metrics_frame(self):
        frame = tk.Frame(self, bg='white', width=538, height=336)
        frame.place(x=0, y=0)

        pressure = 110
        temperature = 27

        # Header
        tk.Label(frame, text="System Metrics", font=('Poppins', 16, 'bold'), bg='white').place(x=20, y=18)
        tk.Label(frame, text="👤", font=('Poppins', 20), bg='white').place(x=482, y=15)

        # Pressure
        self.draw_metric(frame, "110 Psi", "#F58F8F", "#FFD3D3", pressure, 155, 20, 70)

        # Temperature
        self.draw_metric(frame, "27 °C", "#5B93F5", "#A9D0FF", temperature, 50, 20, 140)

        # Leak Rate / Status
        tk.Label(frame, text="Leak Rate:", font=('Poppins', 10, 'bold'), bg='white').place(x=20, y=220)
        tk.Label(frame, text="2.1 x 10⁻⁹", font=('Poppins', 10, 'bold'), fg='green', bg='white').place(x=20, y=245)

        tk.Label(frame, text="Status:", font=('Poppins', 10, 'bold'), bg='white').place(x=250, y=220)
        tk.Label(frame, text="OK", font=('Poppins', 10, 'bold'), fg='green', bg='white').place(x=250, y=245)
        tk.Label(frame, text="✔", font=('Poppins', 18), fg='green', bg='white').place(x=480, y=240)

    def draw_metric(self, parent, label_text, label_color, bar_color, value, max_value, x, y):
        label_width = 92
        bar_width = 414
        height = 50
        radius = 25
        filled_ratio = value / max_value
        filled_width = int(bar_width * filled_ratio)

        # Label box
        label = tk.Canvas(parent, width=label_width, height=height, bg='white', highlightthickness=0)
        label.place(x=x, y=y)
        label.create_rectangle(0, 0, label_width, height, fill=label_color, outline=label_color)
        label.create_text(label_width // 2, height // 2, text=label_text, fill="white", font=('Poppins', 10, 'bold'))

        # Divider
        tk.Frame(parent, width=1, height=height, bg="#C0C0C0").place(x=x + label_width, y=y)

        # Bar canvas
        bar_canvas = tk.Canvas(parent, width=bar_width, height=height, bg='white', highlightthickness=0)
        bar_canvas.place(x=x + label_width + 1, y=y)

        # Gray background
        self.draw_rounded_bar(bar_canvas, 0, 0, bar_width, height, "#EAEAEA", radius)

        # Filled portion
        if filled_width > 0:
            self.draw_rounded_bar(bar_canvas, 0, 0, filled_width, height, bar_color, radius if filled_width >= bar_width else 0)

    def draw_rounded_bar(self, canvas, x, y, width, height, color, round_right=25):
        canvas.create_rectangle(x, y, x + width - round_right, y + height, fill=color, outline=color)
        if round_right > 0:
            canvas.create_arc(x + width - 2 * round_right, y, x + width, y + height,
                              start=270, extent=180, fill=color, outline=color)

    def create_round_rect(self, x1, y1, x2, y2, r=25, **kwargs):
        # Full rounded box for tab
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

        self.configure(bg="#D9D9D9")
        self.place(relwidth=1, relheight=1)

        self.system_metrics = SystemMetrics(self)
        self.system_metrics.place(x=350, y=500)


        # === Sidebar Frame ===
        sidebar_width = 297
        sidebar = tk.Frame(self, bg="#005DAA", width=sidebar_width, height=900)
        sidebar.place(x=0, y=0)

        # === LLNL Circle Logo ===
        try:
            logo = Image.open(self.assets_path / "LLNL Logo Circle.png").resize((170, 170))
            self.logo_img = ImageTk.PhotoImage(logo)
            tk.Label(sidebar, image=self.logo_img, bg="#005DAA").place(x=(sidebar_width - 170) // 2, y=30)
        except:
            tk.Label(sidebar, text="LLNL", bg="#005DAA", fg="white", font=("Poppins", 16)).place(x=20, y=40)

        # === Sidebar Buttons ===
        buttons = [
            ("Dashboard", "Selected Dashboard Button Icon.png"),
            ("Live Data", "Live Data Button Icon.png"),
            ("Run Test", "Run Test Button Icon.png"),
            ("Reports", "Reports Button Icon.png"),
            ("Layout", "Layout Button Icon.png"),
            ("Settings", "Settings Button Icon.png"),
            ("Logout", "Logout Button Icon.png"),
        ]

        base_y = 285  # Start below logo
        spacing = 72

        for i, (text, icon_file) in enumerate(buttons):
            # Add extra 93px after Layout
            if text == "Settings":
                base_y += 150 - spacing

            self.create_sidebar_button(
                parent=sidebar,
                text=text,
                icon_file=icon_file,
                y=base_y + i * spacing,
                sidebar_width=sidebar_width
            )

        # === System Metrics Section ===
        self.system_metrics = SystemMetrics(self)
        self.system_metrics.place(x=350, y=500)  # Adjust positioning as needed

    def create_sidebar_button(self, parent, text, icon_file, y, sidebar_width):
        try:
            icon = Image.open(self.assets_path / icon_file).resize((24, 24))
            icon_img = ImageTk.PhotoImage(icon)
            setattr(self, f"{text.lower().replace(' ', '_')}_icon", icon_img)
        except:
            icon_img = None

        container = tk.Frame(parent, bg="#005DAA", width=250, height=48)
        container.place(x=(sidebar_width - 170) // 2, y=y)

        if icon_img:
            tk.Label(container, image=icon_img, bg="#005DAA").pack(side="left", padx=(0, 30))
        tk.Label(container, text=text, fg="white", bg="#005DAA", font=("Poppins", 12, "bold")).pack(side="left")

