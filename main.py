import tkinter as tk
from pages.dashboard import DashboardPage
from pages.login import LoginPage


class TargetTestingApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("1440x900")
        self.title("Target Testing Station")

        self.container = tk.Frame(self)
        self.container.pack(fill="both", expand=True)

        self.show_dashboard()  # 🚀 directly show dashboard!

    def show_login(self):
        self.clear_frame()
        self.login_page = LoginPage(self.container, self.show_dashboard)
        self.login_page.pack(fill="both", expand=True)

    def show_dashboard(self):
        self.clear_frame()
        self.dashboard_page = DashboardPage(self.container)
        self.dashboard_page.pack(fill="both", expand=True)

    def clear_frame(self):
        for widget in self.container.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    app = TargetTestingApp()
    app.mainloop()
