import tkinter as tk
from pages.dashboard import DashboardPage
from pages.login import LoginPage
from pages.live_data import LiveDataPage
import sys

class TargetTestingApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("1440x900")
        self.title("Target Testing Station")

        self.container = tk.Frame(self, width=1440, height=900)
        self.container.pack(fill="both", expand=True)
        self.container.pack_propagate(False)

        self.username = "admin"  # ✅ Store username for later reuse
        self.show_dashboard(self.username)  # 🚀 Start directly on dashboard

    def show_login(self):
        self.clear_frame()
        self.login_page = LoginPage(self.container, self.show_dashboard)
        self.login_page.place(x=0, y=0)
        self.login_page.update()

    def show_dashboard(self, username):
        self.username = username  # ✅ Update stored username
        self.clear_frame()
        self.dashboard_page = DashboardPage(self.container, controller=self, username=username)
        self.dashboard_page.place(x=0, y=0)

    def show_live_data(self):
        self.clear_frame()
        self.live_data_page = LiveDataPage(self.container, controller=self, username=self.username)
        self.live_data_page.place(x=0, y=0)

    def clear_frame(self):
        for widget in self.container.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    app = TargetTestingApp()
    app.protocol("WM_DELETE_WINDOW", lambda: (app.destroy(), sys.exit()))
    app.mainloop()