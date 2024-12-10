import tkinter as tk
from tkinter import messagebox
import importlib
from Calendar_module import Calendar  # Importing the Calendar class
from today_schedule import today_schedule


class SchedulerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Scheduler App")

        # Top section: Today's Schedule and Calendar
        self.top_frame = tk.Frame(self.root)
        self.top_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Schedule on the left
        self.schedule_frame = tk.Frame(self.top_frame, width=200, bg="lightgrey")
        self.schedule_frame.pack(side="left", fill="both", padx=10, pady=10)
        self.display_today_schedule()

        # Calendar on the right
        self.calendar_frame = tk.Frame(self.top_frame, width=600)
        self.calendar_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)
        self.calendar = Calendar(self.calendar_frame)

        # Bottom section: Navigation Buttons
        self.button_frame = tk.Frame(self.root)
        self.button_frame.pack(fill="x", padx=10, pady=10)
        self.create_buttons()

    def create_buttons(self):
        """Create navigation buttons for various functionalities."""
        # Mapping of use cases to their respective modules
        self.use_cases = {
            "Manage Schedules": "manage_schedules",
            "Filter Events": "filter_events",
            "Set Reminders": "set_reminders",
            "Set Alarms": "set_alarms",
            "Change View (Week/Month)": "change_view",
        }

        for name in self.use_cases.keys():
            tk.Button(self.button_frame, text=name, command=lambda n=name: self.open_use_case(n)).pack(side="left", padx=5)

    def display_today_schedule(self):
        """Display today's schedule in the schedule frame."""
        # Clear any existing content
        for widget in self.schedule_frame.winfo_children():
            widget.destroy()

        # Header
        tk.Label(self.schedule_frame, text="Today's Schedule", font=("Arial", 14), bg="lightgrey").pack(pady=10)

        # Get today's schedule
        schedule = today_schedule.get_today_schedule()

        # Populate schedule
        if schedule:
            for entry in schedule:
                value2 = entry.get("Value2", "N/A")
                value5 = entry.get("Value5", "N/A")
                value7 = entry.get("Value7", "N/A")
                tk.Label(self.schedule_frame, text=f"Subject: {value2}", anchor="w", bg="lightgrey").pack(fill="x", padx=10, pady=2)
                tk.Label(self.schedule_frame, text=f"Class: {value5}", anchor="w", bg="lightgrey").pack(fill="x", padx=10, pady=2)
                tk.Label(self.schedule_frame, text=f"Supervisor: {value7}", anchor="w", bg="lightgrey").pack(fill="x", padx=10, pady=2)
                tk.Frame(self.schedule_frame, height=2, bg="darkgrey").pack(fill="x", pady=5)  # Separator
        else:
            tk.Label(self.schedule_frame, text="No schedule for today.", anchor="center", bg="lightgrey").pack(pady=20)

    def open_use_case(self, use_case_name):
        module_name = self.use_cases[use_case_name]
        try:
            module = importlib.import_module(module_name)
            if hasattr(module, module_name):
                getattr(module, module_name)()
            else:
                messagebox.showerror("Error", f"Function '{module_name}' not found in {module_name}.py")
        except ModuleNotFoundError:
            messagebox.showerror("Error", f"Module '{module_name}' not found.")
        except Exception as e:
            messagebox.showerror("Error", str(e))


if __name__ == "__main__":
    root = tk.Tk()
    app = SchedulerApp(root)
    root.geometry("800x600")
    root.mainloop()
