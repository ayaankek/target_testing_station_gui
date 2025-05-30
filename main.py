import tkinter as tk
from pages.dashboard import DashboardPage
from pages.login import LoginPage
from pages.live_data import LiveDataPage
from pages.run_test import RunTestPage 
from pages.pdd_test import PDDTestPage
from pages.gas_test import GasTestPage
from pages.reports import ReportsPage
from collections import deque

import sys
import threading
import socket

class TargetTestingApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("1440x900")
        self.title("Target Testing Station")

        self.container = tk.Frame(self, width=1440, height=900)
        self.container.pack(fill="both", expand=True)
        self.container.pack_propagate(False)

        self.username = "admin"

        # ✅ Shared buffers
        self.pressure_data = deque([], maxlen=60)
        self.temperature_data = deque([], maxlen=60)
        self.time_data = deque([], maxlen=60)

        self.latest_pressure = 100.0
        self.latest_temperature = 25.0

        self.test_running = True

        threading.Thread(target=self.listen_to_socket, daemon=True).start()
        #self.show_login()
        self.show_dashboard("admin")

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
        
    def listen_to_socket(self, ip='127.0.0.1', port=65432):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((ip, port))
                print("[Socket] ✅ Connected to server")
                while True:
                    data = s.recv(1024)
                    if not data:
                        break
                    decoded = data.decode().strip()
                    parts = decoded.split(',')
                    self.latest_pressure = float(parts[0].split('=')[1])
                    self.latest_temperature = float(parts[1].split('=')[1])

                    t = 0 if not self.time_data else self.time_data[-1] + 1
                    self.pressure_data.append(self.latest_pressure)
                    self.temperature_data.append(self.latest_temperature)
                    self.time_data.append(t)
        
        except Exception as e:
            print("[Socket] ❌ Connection error:", e)

if __name__ == "__main__":
    app = TargetTestingApp()
    app.protocol("WM_DELETE_WINDOW", lambda: (app.destroy(), sys.exit()))
    app.mainloop()