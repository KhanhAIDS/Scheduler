import tkinter as tk
from calendar import monthcalendar, month_name
import datetime


class Calendar:
    """
    A class to display a calendar and allow interaction with specific dates.
    """
    def __init__(self, parent_frame, on_day_click, timetable_manager=None):
        """
        Initialize the calendar.
        :param parent_frame: The parent Tkinter frame to contain the calendar.
        :param on_day_click: Callback function to handle day clicks.
        :param timetable_manager: Optional timetable manager to handle events.
        """
        self.parent_frame = parent_frame
        self.on_day_click = on_day_click  # Function to handle day clicks
        self.timetable_manager = timetable_manager
        self.current_date = datetime.date.today()
        self.calendar_frame = tk.Frame(self.parent_frame, width=600)
        self.calendar_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        self.draw_calendar()

    def draw_calendar(self):
        """Draw the calendar for the current month."""
        for widget in self.calendar_frame.winfo_children():
            widget.destroy()

        # Display current month and year
        tk.Label(self.calendar_frame, text=f"{month_name[self.current_date.month]} {self.current_date.year}",
                 font=("Arial", 16)).pack()

        # Weekdays header
        week_days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        days_frame = tk.Frame(self.calendar_frame)
        days_frame.pack()
        for col, day in enumerate(week_days):
            tk.Label(days_frame, text=day, width=5, font=("Arial", 12), anchor="center").grid(row=0, column=col)

        # Display days of the current month
        days = monthcalendar(self.current_date.year, self.current_date.month)
        for row, week in enumerate(days):
            for col, day in enumerate(week):
                if day == 0:
                    # Empty label for days outside the current month
                    tk.Label(days_frame, text="", width=5).grid(row=row + 1, column=col)
                else:
                    # Check if there are events for this day
                    date_str = f"{self.current_date.year}-{self.current_date.month:02d}-{day:02d}"
                    has_events = False
                    if self.timetable_manager:
                        events = self.timetable_manager.get_events_for_date(date_str)
                        has_events = len(events) > 0

                    # Create button with different background if there are events
                    day_button = tk.Button(
                        days_frame, 
                        text=str(day), 
                        width=5, 
                        font=("Arial", 12),
                        bg="lightblue" if has_events else "white",  # Highlight days with events
                        command=lambda d=day: self.on_day_click(
                            self.current_date.year,
                            self.current_date.month, 
                            d
                        )
                    )
                    day_button.grid(row=row + 1, column=col)

        # Navigation buttons for the calendar
        nav_frame = tk.Frame(self.calendar_frame)
        nav_frame.pack(pady=5)
        tk.Button(nav_frame, text="<<", command=self.previous_month).pack(side="left", padx=5)
        tk.Button(nav_frame, text=">>", command=self.next_month).pack(side="right", padx=5)

    def previous_month(self):
        """Navigate to the previous month."""
        if self.current_date.month == 1:
            self.current_date = self.current_date.replace(year=self.current_date.year - 1, month=12)
        else:
            self.current_date = self.current_date.replace(month=self.current_date.month - 1)
        self.draw_calendar()

    def next_month(self):
        """Navigate to the next month."""
        if self.current_date.month == 12:
            self.current_date = self.current_date.replace(year=self.current_date.year + 1, month=1)
        else:
            self.current_date = self.current_date.replace(month=self.current_date.month + 1)
        self.draw_calendar()