import tkinter as tk
from pages.login import LoginPage  # ✅ Use your login page

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Target Testing Station GUI")
        self.geometry("1440x900")
        self.resizable(False, False)
        self.configure(bg="#002855")

        self.current_page = None
        self.switch_to_login()

    def switch_to_login(self):
        if self.current_page:
            self.current_page.destroy()
        self.current_page = LoginPage(self, self.switch_to_dashboard)
        self.current_page.pack(fill="both", expand=True)

    def switch_to_dashboard(self):
        if self.current_page:
            self.current_page.destroy()
        frame = tk.Frame(self, bg="#F0F0F0")
        tk.Label(frame, text="Dashboard Placeholder", font=("Segoe UI", 24), bg="#F0F0F0").pack(pady=40)
        frame.pack(fill="both", expand=True)
        self.current_page = frame

if __name__ == "__main__":
    app = App()
    app.mainloop()
