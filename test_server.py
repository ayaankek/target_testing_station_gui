import socket
import time
import numpy as np

HOST = '127.0.0.1'
PORT = 65432

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen(1)
    print("✅ Server listening on", HOST, PORT)

    while True:
        conn, addr = s.accept()
        print("🔗 Connected by", addr)
        with conn:
            while True:
                try:
                    pressure = 14 + np.random.rand() * 2
                    temp = 25 + np.random.rand() * 4
                    msg = f"pressure={pressure:.2f},temperature={temp:.2f}\n"
                    conn.sendall(msg.encode())
                    print("📤 Sent:", msg.strip())
                    time.sleep(5)
                except ConnectionResetError:
                    print("❌ Connection lost. Rewaiting for a new client...")
                    break



