import tkinter as tk
from tkinter import ttk
from Calendar_module import Calendar
from configure_day import ConfigureDay  # Import the ConfigureDay class
from timetable_manager import TimetableManager
from datetime import datetime

class SchedulerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Scheduler App")
        
        # Initialize timetable manager first and load data
        self.timetable_manager = TimetableManager()
        if not self.load_timetable():
            print("Warning: No timetable data loaded")

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
        self.display_today_schedule()  # Now safe to call after timetable_manager is initialized

        # Calendar on the right
        self.calendar_frame = tk.Frame(self.top_frame, width=600)
        self.calendar_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)
        # Pass timetable_manager to Calendar
        self.calendar = Calendar(self.calendar_frame, self.open_configure_day, self.timetable_manager)

        # Bottom section: Navigation Buttons
        self.button_frame = tk.Frame(self.root)
        self.button_frame.pack(fill="x", padx=10, pady=10)
        self.create_buttons()

    def create_buttons(self):
        """Create navigation buttons for various functionalities."""
        tk.Button(self.button_frame, text="Manage Events", font=("Arial", 12), command=self.manage_events).pack(
            side="left", padx=5)

    def load_timetable(self):
        """Load timetable and generate semester events"""
        try:
            print("Attempting to load timetable data...")
            if self.timetable_manager.load_timetable("table_data.json"):
                print("Timetable data loaded successfully")
                print(f"Number of courses loaded: {len(self.timetable_manager.timetable_data)}")
                
                # Configure your semester dates
                self.timetable_manager.generate_semester_events(
                    start_date="2024-01-22",
                    end_date="2024-05-31"
                )
                print(f"Generated {len(self.timetable_manager.semester_events)} semester events")
                return True
            else:
                print("Failed to load timetable data")
                return False
        except Exception as e:
            print(f"Error loading timetable: {e}")
            return False

    def display_today_schedule(self):
        """Display today's schedule in the schedule frame"""
        for widget in self.schedule_frame.winfo_children():
            widget.destroy()

        today = datetime.now().strftime("%Y-%m-%d")
        print(f"\nFetching events for {today}")
        
        events = self.timetable_manager.get_events_for_date(today)
        print(f"Found {len(events)} events for today")

        tk.Label(self.schedule_frame, text="Today's Schedule", 
                font=("Arial", 14), bg="lightgrey").pack(pady=10)

        if not events:
            no_events_label = tk.Label(self.schedule_frame, 
                                     text="No schedule for today.\nMake sure table_data.json exists and contains data.", 
                                     font=("Arial", 12), bg="lightgrey", wraplength=180)
            no_events_label.pack(pady=20)
        else:
            for event in events:
                event_frame = tk.Frame(self.schedule_frame, bg="white", relief="raised", borderwidth=1)
                event_frame.pack(fill="x", pady=5, padx=5)
                
                tk.Label(event_frame, text=event.event_name, 
                        font=("Arial", 12, "bold"), bg="white").pack(anchor="w", padx=5, pady=2)
                tk.Label(event_frame, text=event.event_timeframe.split(" ")[1],  # Show only time part
                        font=("Arial", 10), bg="white").pack(anchor="w", padx=5)
                if event.event_note:
                    tk.Label(event_frame, text=event.event_note, 
                            font=("Arial", 10), bg="white", fg="gray").pack(anchor="w", padx=5, pady=2)

    def open_configure_day(self, year, month, day):
        """Open ConfigureDay for the selected date."""
        selected_date = f"{year}-{month:02d}-{day:02d}"
        configure_window = tk.Toplevel(self.root)
        configure_window.title(f"Configure Day: {selected_date}")
        
        # Get events for the selected date
        events = self.timetable_manager.get_events_for_date(selected_date)
        
        # Create ConfigureDay instance and pass the events
        config_day = ConfigureDay(configure_window)
        
        # Add existing events to the ConfigureDay
        for event in events:
            config_day.event_list.append(event)
            config_day.event_listbox.insert(tk.END, event.event_name)

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