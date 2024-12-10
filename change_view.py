
import tkinter as tk
from tkinter import messagebox

def change_view():
    window = tk.Tk()
    window.title("Change View")
    window.geometry("400x300")

    def set_week_view():
        messagebox.showinfo("Action", "Switched to Week View")

    def set_month_view():
        messagebox.showinfo("Action", "Switched to Month View")

    tk.Button(window, text="Week View", command=set_week_view).pack(pady=10)
    tk.Button(window, text="Month View", command=set_month_view).pack(pady=10)
    tk.Button(window, text="Close", command=window.destroy).pack(pady=10)

    window.mainloop()
