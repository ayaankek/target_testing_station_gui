import tkinter as tk
from pages.dashboard import DashboardPage
from pages.login import LoginPage
from pages.live_data import LiveDataPage
from pages.run_test import RunTestPage 
from pages.pdd_test import PDDTestPage
from pages.gas_test import GasTestPage
from pages.reports import ReportsPage

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
        #self.show_dashboard("admin")  # 🚀 Start directly on dashboard
        #self.show_login()
        self.show_reports()
        self.test_running = True

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

    def show_run_test(self, username):
        self.username = username
        self.clear_frame()
        self.run_test_page = RunTestPage(self.container, controller=self, username=username)
        self.run_test_page.place(x=0, y=0)

    def clear_frame(self):
        for widget in self.container.winfo_children():
            widget.destroy()
         
    def show_pdd_test(self):
        self.clear_frame()
        self.pdd_test_page = PDDTestPage(self.container)
        self.pdd_test_page.place(x=0, y=0, width=1440, height=900)  # ✅ ADD WIDTH + HEIGHT

    def show_gas_test(self):
        self.clear_frame()
        self.gas_test_page = GasTestPage(self.container, controller=self, username=self.username)
        self.gas_test_page.place(x=0, y=0, width=1440, height=900)  # ✅ THIS LINE IS REQUIRED

    def show_reports(self):
        self.clear_frame()
        self.reports_page = ReportsPage(self.container, controller=self, username=self.username)
        self.reports_page.place(x=0, y=0, width=1440, height=900)

    def get_chamber_data(self):
        if hasattr(self, 'live_data_page'):
            return self.live_data_page.get_chamber_data()
        else:
            print("⚠️ Live data page not initialized.")
            return []


if __name__ == "__main__":
    app = TargetTestingApp()
    app.protocol("WM_DELETE_WINDOW", lambda: (app.destroy(), sys.exit()))
    app.mainloop()