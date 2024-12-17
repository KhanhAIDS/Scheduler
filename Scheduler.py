import tkinter as tk
from tkinter import ttk
from Calendar_module import Calendar
from configure_day import ConfigureDay  # Import the ConfigureDay class


class SchedulerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Scheduler App")

        # Top section: View Options Dropdown
        self.view_frame = tk.Frame(self.root)
        self.view_frame.pack(fill="x", padx=10, pady=10)

        tk.Label(self.view_frame, text="View:", font=("Arial", 12)).pack(side="left", padx=5)
        self.view_var = tk.StringVar(value="Month")
        self.view_dropdown = ttk.Combobox(self.view_frame, textvariable=self.view_var, state="readonly",
                                          values=["Week", "Month", "Year"], font=("Arial", 12))
        self.view_dropdown.pack(side="left")
        self.view_dropdown.bind("<<ComboboxSelected>>", self.on_view_change)

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
        self.calendar = Calendar(self.calendar_frame, self.open_configure_day)

        # Bottom section: Navigation Buttons
        self.button_frame = tk.Frame(self.root)
        self.button_frame.pack(fill="x", padx=10, pady=10)
        self.create_buttons()

    def create_buttons(self):
        """Create navigation buttons for various functionalities."""
        tk.Button(self.button_frame, text="Manage Events", font=("Arial", 12), command=self.manage_events).pack(
            side="left", padx=5)

    def display_today_schedule(self):
        """Display today's schedule in the schedule frame."""
        # Placeholder for showing today's schedule
        for widget in self.schedule_frame.winfo_children():
            widget.destroy()

        tk.Label(self.schedule_frame, text="Today's Schedule", font=("Arial", 14), bg="lightgrey").pack(pady=10)
        tk.Label(self.schedule_frame, text="No schedule for today.", font=("Arial", 12), bg="lightgrey").pack(pady=20)

    def open_configure_day(self, year, month, day):
        """Open ConfigureDay for the selected date."""
        selected_date = f"{year}-{month:02d}-{day:02d}"
        configure_window = tk.Toplevel(self.root)
        configure_window.title(f"Configure Day: {selected_date}")
        ConfigureDay(configure_window)

    def manage_events(self):
        """Placeholder for managing events."""
        print("Manage Events clicked.")

    def on_view_change(self, event):
        """Handle view changes based on the dropdown selection."""
        selected_view = self.view_var.get()
        if selected_view == "Week":
            print("Switched to Week View (not implemented yet).")
        elif selected_view == "Month":
            print("Switched to Month View.")
        elif selected_view == "Year":
            print("Switched to Year View (not implemented yet).")


if __name__ == "__main__":
    root = tk.Tk()
    app = SchedulerApp(root)
    root.geometry("1000x700")
    root.mainloop()