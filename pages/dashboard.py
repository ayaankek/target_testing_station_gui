import tkinter as tk
from PIL import Image, ImageTk
from pathlib import Path

class DashboardPage(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.assets_path = Path(__file__).resolve().parent.parent / "assets"

        self.configure(bg="white")
        self.place(relwidth=1, relheight=1)

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

        base_y = 275  # Start below logo
        spacing = 72

        for i, (text, icon_file) in enumerate(buttons):
            # Add extra 93px after Layout
            if text == "Settings":
                base_y += 93 - spacing

            self.create_sidebar_button(
                parent=sidebar,
                text=text,
                icon_file=icon_file,
                y=base_y + i * spacing,
                sidebar_width=sidebar_width
            )

    def create_sidebar_button(self, parent, text, icon_file, y, sidebar_width):
        try:
            icon = Image.open(self.assets_path / icon_file).resize((24, 24))
            icon_img = ImageTk.PhotoImage(icon)
            setattr(self, f"{text.lower().replace(' ', '_')}_icon", icon_img)
        except:
            icon_img = None

        container = tk.Frame(parent, bg="#005DAA", width=250, height=48)
        container.place(x=(sidebar_width - 200) // 2, y=y)

        if icon_img:
            tk.Label(container, image=icon_img, bg="#005DAA").pack(side="left", padx=(0, 30))
        tk.Label(container, text=text, fg="white", bg="#005DAA", font=("Poppins", 12, "bold")).pack(side="left")
