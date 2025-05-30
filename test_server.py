import socket
import time
import numpy as np

HOST = '127.0.0.1'
PORT = 65432

base_pressure = 100
decay_rate = 0.03
t = 0

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen(1)
    print("✅ Server listening on", HOST, PORT)

    while True:
        conn, addr = s.accept()
        print("🔗 Connected by", addr)
        with conn:
            t = 0
            while True:
                try:
                    # Base exponential decay
                    pressure = base_pressure * np.exp(-decay_rate * t)

                    # Add periodic drops and random spikes to simulate leak/fall
                    pressure += 5 * np.sin(t / 2)  # wavy pattern
                    pressure += np.random.normal(0, 1.5)  # random spikes
                    pressure = max(0, min(pressure, 145))  # Clamp to 0–145 psi

                    temperature = 25 + np.sin(t / 8) + np.random.normal(0, 0.5)

                    msg = f"pressure={pressure:.2f},temperature={temperature:.2f}\n"
                    conn.sendall(msg.encode())
                    print("📤 Sent:", msg.strip())

                    t += 1
                    time.sleep(5)
                except ConnectionResetError:
                    print("❌ Connection lost. Rewaiting for a new client...")
                    break




