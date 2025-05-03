import tkinter as tk
from PIL import Image, ImageTk
from pathlib import Path

class SideMenu(tk.Frame):
    def __init__(self, parent, controller, active_page="Dashboard", username="Guest"):
        super().__init__(parent, bg="#005DAA", width=int(0.2 * 1440), height=900)
        self.controller = controller
        self.active_page = active_page
        self.username = username  # ✅ store it
        self.assets_path = Path(__file__).resolve().parent.parent / "assets"
        self.place(x=0, y=0)

        self.build_sidebar()

    def build_sidebar(self):
        try:
            logo = Image.open(self.assets_path / "LLNL Logo Circle.png").resize((170, 170))
            self.logo_img = ImageTk.PhotoImage(logo)
            tk.Label(self, image=self.logo_img, bg="#005DAA").place(x=(self.winfo_reqwidth() - 170) // 2, y=30)
        except:
            tk.Label(self, text="LLNL", bg="#005DAA", fg="white", font=('Poppins', 16)).place(x=20, y=40)

        buttons = [
            {
                "text": "Dashboard",
                "icon": "SelectedDashboardButtonIcon.png" if self.active_page == "Dashboard" else "DashboardButtonIcon.png",
                "command": lambda: self.controller.show_dashboard(self.username)
            },
            {
                "text": "Live Data",
                "icon": "SelectedLiveDataButtonIcon.png" if self.active_page == "Live Data" else "LiveDataButtonIcon.png",
                "command": self.controller.show_live_data
            },
            {
                "text": "Run Test", "icon": "Run Test Button Icon.png", "command": None
            },
            {
                "text": "Reports", "icon": "Reports Button Icon.png", "command": None
            },
            {
                "text": "Layout", "icon": "Layout Button Icon.png", "command": None
            },
            {
                "text": "Settings", "icon": "Settings Button Icon.png", "command": None
            },
            {
                "text": "Logout", "icon": "Logout Button Icon.png", "command": self.controller.show_login
            },
        ]


        base_y = 285
        spacing = 72

        try:
            bar_icon = Image.open(self.assets_path / "SideMenuSelectionButton.png").resize((8, 48))
            self.sidebar_bar_img = ImageTk.PhotoImage(bar_icon)
        except:
            self.sidebar_bar_img = None

        for i, button in enumerate(buttons):
            if button["text"] == "Settings":
                base_y += 150 - spacing
            y = base_y + i * spacing
            self.create_button(button["text"], button["icon"], y, button["command"])

            if button["text"] == self.active_page and self.sidebar_bar_img:
                tk.Label(self, image=self.sidebar_bar_img, bg="#005DAA").place(x=0, y=y)

    def create_button(self, text, icon_file, y, command=None):
        try:
            icon = Image.open(self.assets_path / icon_file).resize((24, 24))
            icon_img = ImageTk.PhotoImage(icon)
            setattr(self, f"{text.lower().replace(' ', '_')}_icon", icon_img)
        except:
            icon_img = None

        frame = tk.Frame(self, bg="#005DAA", width=250, height=48)
        frame.place(x=(self.winfo_reqwidth() - 170) // 2, y=y)

        if icon_img:
            tk.Label(frame, image=icon_img, bg="#005DAA").pack(side="left", padx=(0, 30))

        if text in ["Settings", "Logout"] or text == self.active_page:
            fg_color = "white"
        else:
            fg_color = "#6E94C8"

        label = tk.Label(frame, text=text, font=("Poppins", 12, "bold"), fg=fg_color, bg="#005DAA")
        label.pack(side="left")

        if command:
            def handle_click(event):
                command()
            frame.bind("<Button-1>", handle_click)
            label.bind("<Button-1>", handle_click)

