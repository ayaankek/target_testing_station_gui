import tkinter as tk
from PIL import Image, ImageTk
from pathlib import Path
import numpy as np
from collections import deque
import threading
import socket
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from pages.side_menu import SideMenu
from pages.dashboard import ChamberData


class TargetChamber(tk.Canvas):
    def __init__(self, parent):
        width = 306
        height = 405
        super().__init__(parent, width=width, height=height, bg="#D9D9D9", highlightthickness=0)
        self.width = width
        self.height = height
        self.assets_path = Path(__file__).resolve().parent.parent / "assets"

        self.icon_img = None
        try:
            icon = Image.open(self.assets_path / "hugeicons_gas-pipe.png").resize((35, 35))
            self.icon_img = ImageTk.PhotoImage(icon)
        except:
            pass

    def embed_vertical_metrics(self, temperature, pressure):
        for widget in self.winfo_children():
            widget.destroy()

        frame = tk.Frame(self, bg="white", width=self.width, height=self.height)
        frame.place(x=0, y=0)

        tk.Label(frame, text="Target Chamber", font=('Poppins', 16, 'bold'), bg="white").place(x=20, y=20)
        if self.icon_img:
            tk.Label(frame, image=self.icon_img, bg="white").place(x=self.width - 50, y=20)

        bar_width = 80
        bar_height = 210
        label_height = 58
        spacing = 30
        total_width = 2 * bar_width + spacing
        total_height = bar_height + label_height + 10

        start_x = (self.width - total_width) // 2
        start_y = (self.height - total_height) // 2 + 30

        self.draw_vertical_metric(frame, f"{pressure:.2f} Pa", "#F58F8F", "#FFD3D3", pressure, 155, x=start_x, y=start_y, bar_width=bar_width, bar_height=bar_height)
        self.draw_vertical_metric(frame, f"{temperature:.2f} °C", "#5B93F5", "#A9D0FF", temperature, 50, x=start_x + bar_width + spacing, y=start_y, bar_width=bar_width, bar_height=bar_height)

    def draw_vertical_metric(self, parent, label_text, label_color, bar_color, value, max_value, x, y, bar_width=60, bar_height=200):
        label_height = 58
        radius = 30
        filled_ratio = min(value / max_value, 1.0)
        filled_height = int(bar_height * filled_ratio)

        label_canvas = tk.Canvas(parent, width=bar_width, height=label_height, bg="white", highlightthickness=0)
        label_canvas.place(x=x, y=y + bar_height)
        label_canvas.create_rectangle(0, 0, bar_width, label_height, fill=label_color, outline=label_color)
        label_canvas.create_text(bar_width // 2, label_height // 2, text=label_text, fill="white", font=('Poppins', 12, 'bold'))

        bar_canvas = tk.Canvas(parent, width=bar_width, height=bar_height, bg="white", highlightthickness=0)
        bar_canvas.place(x=x, y=y)
        bar_canvas.create_rectangle(0, radius, bar_width, bar_height, fill="#EAEAEA", outline="#EAEAEA")
        bar_canvas.create_arc(0, 0, bar_width, 2 * radius, start=0, extent=180, fill="#EAEAEA", outline="#EAEAEA")

        if filled_height > 0:
            y_fill = bar_height - filled_height
            bar_canvas.create_rectangle(0, y_fill, bar_width, bar_height, fill=bar_color, outline=bar_color)


class LiveDataPage(tk.Frame):
    def __init__(self, master, controller, username="admin"):
        super().__init__(master)
        self.controller = controller
        self.username = username

        self.window_width = 1440
        self.window_height = 900
        self.sidebar_width = int(0.2 * self.window_width)

        self.configure(bg="#D9D9D9")
        self.place(width=self.window_width, height=self.window_height)

        self.live_data_area = tk.Frame(self, bg="#D9D9D9", width=self.window_width - self.sidebar_width, height=self.window_height)
        self.live_data_area.place(x=self.sidebar_width, y=0)

        self.sidebar = SideMenu(self, controller=self.controller, active_page="Live Data")

        self.chamber_data = ChamberData(self.live_data_area)
        self.chamber_data.place(x=50, y=90)

        self.target_chamber = TargetChamber(self.live_data_area)
        self.target_chamber.place(x=795, y=90)

        self.leak_test = LeakTest(self.live_data_area)
        self.leak_test.place(x=50, y=530) #adjust y if needed

        self.rate_fall_test = RateOfFallTest(self.live_data_area)
        self.rate_fall_test.place(x=602, y=520) #adjust x/y as needed`

        self.time_data = deque([], maxlen=60)
        self.pressure_data = deque([], maxlen=60)
        self.temperature_data = deque([], maxlen=60)

        self.latest_pressure = 15
        self.latest_temperature = 28
        self.test_running = True

        #self.live_data_page = LiveDataPage(self.container, self, self.username)

        # Fallback test data for graphs
        leak_time = np.linspace(0, 12, 15)
        leak_pressure = 16 - 2 * np.abs(np.sin(leak_time / 3))
        self.leak_test.update_graph(leak_time.tolist(), leak_pressure.tolist())

        fall_time = np.linspace(0, 12, 15)
        fall_pressure = 16 * np.exp(-fall_time / 6) + 14
        self.rate_fall_test.update_graph(fall_time.tolist(), fall_pressure.tolist())

        x_start = self.window_width - self.sidebar_width - 200
        tk.Label(self.live_data_area, text="Logged in as:", font=("Poppins", 11), fg="#333", bg="#D9D9D9").place(x=x_start, y=20)
        tk.Label(self.live_data_area, text=self.username, font=("Poppins", 12, "bold"), fg="#333", bg="#D9D9D9").place(x=x_start + 110, y=19)

        self.start_button = tk.Button(
            self.live_data_area,
            text="▶ Start Test",
            font=("Poppins", 10, "bold"),
            bg="#5B93F5",
            fg="white",
            relief="flat",
            command=self.start_test
        )
        self.start_button.place(x=x_start - 120, y=16, width=90, height=28)

        self.stop_button = tk.Button(
            self.live_data_area,
            text="⏹ Stop Test",
            font=("Poppins", 10, "bold"),
            bg="#F58F8F",
            fg="white",
            relief="flat",
            command=self.stop_test
        )
        self.stop_button.place(x=x_start - 220, y=16, width=90, height=28)

        tk.Label(self.live_data_area, text="Live Data", font=("Poppins", 24, "bold"), bg="#D9D9D9").place(x=45, y=15)

        threading.Thread(target=self.listen_to_socket, daemon=True).start()
        self.update_live_data()

    def listen_to_socket(self, ip='127.0.0.1', port=65432):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((ip, port))
                print("[Socket] ✅ Connected to server at", ip, port)
                while True:
                    data = s.recv(1024)
                    if not data:
                        break
                    decoded = data.decode().strip()
                    print("[Socket] 📥", decoded)
                    try:
                        parts = decoded.split(',')
                        self.latest_pressure = float(parts[0].split('=')[1])
                        self.latest_temperature = float(parts[1].split('=')[1])
                    except Exception as e:
                        print("⚠️ Bad socket data:", decoded, "|", e)
        except Exception as e:
            print("[Socket] ❌", e)

    def update_live_data(self):
        if not self.test_running:
            return
        pressure = self.latest_pressure
        temperature = self.latest_temperature

        self.pressure_data.append(pressure)
        self.temperature_data.append(temperature)
        self.time_data.append(0 if not self.time_data else self.time_data[-1] + 1)

        print(f"[Graph] Pressure={pressure:.2f} at t={self.time_data[-1]}")

        self.chamber_data.update_graph(list(self.time_data), list(self.pressure_data))
        self.target_chamber.embed_vertical_metrics(temperature, pressure)

        self.after(5000, self.update_live_data)

    def stop_test(self):
        self.test_running = False

    def start_test(self):
        if not self.test_running:
            self.test_running = True
            self.update_live_data()

    def get_chamber_data(self):
        return list(zip(self.time_data, self.pressure_data, self.temperature_data))

class LeakTest(tk.Canvas):
    def __init__(self, parent):
        super().__init__(parent, width=500, height=333, bg="#D9D9D9", highlightthickness=0)
        self.assets_path = Path(__file__).resolve().parent.parent / "assets"

    def update_graph(self, time_data, pressure_data):
        for widget in self.winfo_children():
            widget.destroy()

        frame = tk.Frame(self, bg='white', width=500, height=333)
        frame.place(x=0, y=0)

        tk.Label(frame, text="Leak Test", font=('Poppins', 16, 'bold'), bg='white').place(x=25, y=18)

        fig, ax = plt.subplots(figsize=(5.8, 2.8))
        ax.plot(time_data, pressure_data, color='blue', marker='o')
        ax.set_xlabel('Time (mins)')
        ax.set_ylabel('Pressure (Psi)')
        ax.grid(True)
        fig.tight_layout()

        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.draw()
        plt.close(fig)
        canvas.get_tk_widget().place(x=20, y=60, width=460, height=250)


class RateOfFallTest(LeakTest):
    def update_graph(self, time_data, pressure_data):
        super().update_graph(time_data, pressure_data)
        for widget in self.winfo_children():
            if isinstance(widget, tk.Frame):
                tk.Label(widget, text="Rate of Fall Test", font=('Poppins', 16, 'bold'), bg='white').place(x=25, y=18)