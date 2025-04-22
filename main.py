import tkinter as tk

window = tk.Tk()
window.title("Hello GUI")
window.geometry("400x300")
tk.Label(window, text="Target Testing Station", font=("Arial", 16)).pack(pady=20)
window.mainloop()
