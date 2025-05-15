import tkinter as tk
from PIL import Image, ImageTk
from pathlib import Path
import numpy as np
from collections import deque
import threading
import socket
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
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

        # Default values
        self.latest_temperature = 28
        self.latest_pressure = 15

        # Start socket listener in background
        threading.Thread(target=self.listen_to_socket, daemon=True).start()

        # Start UI refresh loop
        self.refresh_display()

    def listen_to_socket(self, ip='127.0.0.1', port=65432):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((ip, port))
                print("[TargetChamber] Connected to server")

                while True:
                    data = s.recv(1024)
                    if not data:
                        break

                    decoded = data.decode().strip()
                    try:
                        parts = decoded.split(',')
                        self.latest_pressure = float(parts[0].split('=')[1])
                        self.latest_temperature = float(parts[1].split('=')[1])
                        print(f"[TargetChamber] Updated: {self.latest_pressure:.2f} psi, {self.latest_temperature:.2f} °C")
                    except Exception as e:
                        print("TargetChamber Parse Error:", decoded, "|", e)
        except Exception as e:
            print("[TargetChamber] Socket error:", e)

    def refresh_display(self):
        self.embed_vertical_metrics(self.latest_temperature, self.latest_pressure)
        self.after(5000, self.refresh_display)

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
        self.leak_test.place(x=50, y=530)

        self.rate_fall_test = RateOfFallTest(self.live_data_area)
        self.rate_fall_test.place(x=602, y=530)

        # Fallback for Leak Test — Sine wave (simulating leak detection peak)
        leak_time = np.linspace(0, 12, 15)  # 0 to 12 minutes
        leak_pressure = 16 - 2 * np.abs(np.sin(leak_time / 3))  # peak in the middle
        self.leak_test.update_graph(leak_time.tolist(), leak_pressure.tolist())

        # Fallback for Rate of Fall Test — Exponential decay
        fall_time = np.linspace(0, 12, 15)
        fall_pressure = 16 * np.exp(-fall_time / 6) + 14  # slow fall-off from 30 → 14
        self.rate_fall_test.update_graph(fall_time.tolist(), fall_pressure.tolist())

        tk.Label(self.live_data_area, text="Live Data", font=("Poppins", 24, "bold"), bg="#D9D9D9").place(x=45, y=15)

        x_start = self.window_width - self.sidebar_width - 200
        tk.Label(self.live_data_area, text="Logged in as:", font=("Poppins", 11), fg="#333", bg="#D9D9D9").place(x=x_start, y=20)
        tk.Label(self.live_data_area, text=self.username, font=("Poppins", 12, "bold"), fg="#333", bg="#D9D9D9").place(x=x_start + 110, y=19)

        # Stop Button
        self.stop_button = tk.Button(
            self.live_data_area,
            text="⏹ Stop Test",
            font=("Poppins", 10, "bold"),
            bg="#F58F8F",
            fg="white",
            relief="flat",
            command=self.stop_test
        )
        self.stop_button.place(x=x_start - 150, y=16, width=100, height=28)

        self.time_data = deque([], maxlen=60)
        self.pressure_data = deque([], maxlen=30)

        self.latest_temperature = 28
        self.latest_pressure = 15

        threading.Thread(target=self.listen_to_socket, daemon=True).start()
        self.update_live_data()

    def listen_to_socket(self, ip='127.0.0.1', port=65432):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((ip, port))
                print("[Socket] Connected to server at", ip, port)

                while True:
                    data = s.recv(1024)
                    if not data:
                        break  # exit loop before using decoded

                    decoded = data.decode().strip()
                    print("[Socket] Raw data received:", decoded)  # ✅ Moved inside

                    try:
                        if '=' in decoded:
                            parts = decoded.split(',')
                            pressure_val = float(parts[0].split('=')[1])
                            temp_val = float(parts[1].split('=')[1])
                        else:
                            pressure_val, temp_val = map(float, decoded.split(','))

                        self.latest_pressure = pressure_val
                        self.latest_temperature = temp_val
                        print(f"[Socket] Updated → Pressure: {pressure_val:.2f} psi | Temp: {temp_val:.2f} °C")

                    except (IndexError, ValueError) as e:
                        print("Malformed TCP data:", decoded, "| Error:", e)

        except Exception as e:
            print("Socket connection error:", e)


    def update_live_data(self):
        if not self.controller.test_running:
            return  # 🚫 Stop updating

        temperature = self.latest_temperature
        pressure = self.latest_pressure if self.latest_pressure is not None else 0

        self.pressure_data.append(pressure)
        self.time_data.append(0 if len(self.time_data) == 0 else self.time_data[-1] + 1)

        self.chamber_data.update_graph(list(self.time_data), list(self.pressure_data))
        self.target_chamber.embed_vertical_metrics(temperature, pressure)

        self.after(60000, self.update_live_data)

    def stop_test(self):
        self.controller.test_running = False
        print("🛑 Test stopped.")

class LeakTest(tk.Canvas):
    def __init__(self, parent):
        width = 500
        height = 333
        super().__init__(parent, width=width, height=height, bg="#D9D9D9", highlightthickness=0)
        self.width = width
        self.height = height
        self.assets_path = Path(__file__).resolve().parent.parent / "assets"
        self.place(x=0, y=0)

    def update_graph(self, time_data, pressure_data):
        for widget in self.winfo_children():
            widget.destroy()

        frame = tk.Frame(self, bg='white', width=self.width, height=self.height)
        frame.place(x=0, y=0)

        tk.Label(frame, text="Leak Test", font=('Poppins', 16, 'bold'), bg='white').place(x=25, y=18)

        try:
            icon = Image.open(self.assets_path / "ChamberDataIcon.png").resize((40, 40))
            self.expand_icon_img = ImageTk.PhotoImage(icon)
            tk.Label(frame, image=self.expand_icon_img, bg='white').place(x=self.width - 60, y=20)
        except:
            pass

        fig, ax = plt.subplots(figsize=(5.8, 2.8))
        ax.plot(time_data, pressure_data, color='blue', marker='o')
        ax.set_xlabel('Time (mins)')
        ax.set_ylabel('Pressure (Psi)')
        ax.set_xlim(left=0)
        ax.grid(True)
        fig.tight_layout()

        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.draw()
        plt.close(fig)
        canvas.get_tk_widget().place(x=20, y=60, width=self.width - 40, height=self.height - 80)

class RateOfFallTest(tk.Canvas):
    def __init__(self, parent):
        width = 500
        height = 333
        super().__init__(parent, width=width, height=height, bg="#D9D9D9", highlightthickness=0)
        self.width = width
        self.height = height
        self.assets_path = Path(__file__).resolve().parent.parent / "assets"
        self.place(x=0, y=0)

    def update_graph(self, time_data, pressure_data):
        for widget in self.winfo_children():
            widget.destroy()

        frame = tk.Frame(self, bg='white', width=self.width, height=self.height)
        frame.place(x=0, y=0)

        tk.Label(frame, text="Rate of Fall Test", font=('Poppins', 16, 'bold'), bg='white').place(x=25, y=18)

        try:
            icon = Image.open(self.assets_path / "ChamberDataIcon.png").resize((40, 40))
            self.expand_icon_img = ImageTk.PhotoImage(icon)
            tk.Label(frame, image=self.expand_icon_img, bg='white').place(x=self.width - 60, y=20)
        except:
            pass

        fig, ax = plt.subplots(figsize=(5.8, 2.8))
        ax.plot(time_data, pressure_data, color='blue', marker='o')
        ax.set_xlabel('Time (mins)')
        ax.set_ylabel('Pressure (Psi)')
        ax.grid(True)
        fig.tight_layout()

        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.draw()
        plt.close(fig)
        canvas.get_tk_widget().place(x=20, y=60, width=self.width - 40, height=self.height - 80)
