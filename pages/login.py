import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from pathlib import Path


class LoginPage(tk.Frame):
    def __init__(self, master, switch_to_dashboard):
        super().__init__(master, bg="#002855")
        self.switch_to_dashboard = switch_to_dashboard
        self.assets_path = Path(__file__).resolve().parent.parent / "assets"

        # === Canvas Background ===
        canvas = tk.Canvas(self, bg="#002855", height=900, width=1440, bd=0, highlightthickness=0, relief="ridge")
        canvas.place(x=0, y=0)

        # === White login panel (Right side) ===
        canvas.create_rectangle(480, 0, 1440, 1024, fill="white", outline="")

        # === LLNL Logo ===
        try:
            llnl_image = Image.open(self.assets_path / "LLNL Logo.png").resize((747, 144))
            self.llnl_img = ImageTk.PhotoImage(llnl_image)
            canvas.create_image(960, 150, image=self.llnl_img)
        except:
            canvas.create_text(960, 100, text="LLNL Logo", fill="#000", font=("Segoe UI", 20))

        # === USERNAME Entry ===
        self.username = self.create_input_with_icon(
            icon_file="user.png",
            placeholder="USERNAME",
            x=720,
            y=83 + 144 + 196  # 196px below logo bottom
        )

        # === PASSWORD Entry ===
        self.password = self.create_input_with_icon(
            icon_file="lock.png",
            placeholder="PASSWORD",
            x=720,
            y=83 + 144 + 196 + 66 + 29  # 29px below username
        )

        # === LOGIN Button ===
        login_y = 83 + 144 + 196 + 66 + 29 + 66 + 57
        login_btn = tk.Button(
            self,
            text="LOGIN",
            bg="#275ea7",
            fg="white",
            font=("Segoe UI", 11, "bold"),
            bd=0,
            command=self.authenticate
        )
        login_btn.place(x=720, y=login_y, width=442, height=66)

        # === Forgot Password ===
        canvas.create_text(720 + 390, login_y + 66 + 16, text="Forgot password?", fill="#275ea7", font=("Segoe UI", 9))

        # === UC Davis Seal ===
        try:
            seal_image = Image.open(self.assets_path / "ucdavis-seal.png").resize((241, 241))
            self.seal_img = ImageTk.PhotoImage(seal_image)
            canvas.create_image(475, 780, image=self.seal_img)
        except:
            canvas.create_text(160, 780, text="UC Davis", fill="white", font=("Segoe UI", 18))

    def create_input_with_icon(self, icon_file, placeholder, x, y):
        """Creates a single-line input with an icon on the left"""
        container = tk.Frame(self, bg="white", highlightbackground="#517db8", highlightthickness=1)
        container.place(x=x, y=y, width=442, height=66)

        # Icon
        try:
            icon = Image.open(self.assets_path / icon_file).resize((27, 27))
            icon_img = ImageTk.PhotoImage(icon)
            setattr(self, f"{placeholder.lower()}_icon", icon_img)
            tk.Label(container, image=icon_img, bg="white").place(x=29, y=19)
        except:
            fallback = "👤" if "user" in icon_file else "🔒"
            tk.Label(container, text=fallback, font=("Segoe UI", 12), bg="white").place(x=29, y=19)

        # Entry Field
        entry = tk.Entry(container, font=("Segoe UI", 11), bd=0, fg="gray")
        entry.insert(0, placeholder)
        entry.place(x=125, y=18, width=290, height=30)
        entry.placeholder = placeholder
        entry.is_password = placeholder == "PASSWORD"

        # Events
        entry.bind("<FocusIn>", lambda e: self._clear_placeholder(entry))
        entry.bind("<FocusOut>", lambda e: self._restore_placeholder(entry))

        return entry

    def _clear_placeholder(self, entry):
        if entry.get() == entry.placeholder:
            entry.delete(0, tk.END)
            entry.config(fg="#517db8")
            if entry.is_password:
                entry.config(show="*")

    def _restore_placeholder(self, entry):
        if not entry.get():
            entry.insert(0, entry.placeholder)
            entry.config(fg="gray")
            if entry.is_password:
                entry.config(show="")

    def authenticate(self):
        username = self.username.get()
        password = self.password.get()
        if username == "admin" and password == "1234":
            self.switch_to_dashboard()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")
