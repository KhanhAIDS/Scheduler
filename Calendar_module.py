import tkinter as tk
from calendar import monthcalendar, month_name
import datetime

class Calendar:
    def __init__(self, parent_frame):
        self.parent_frame = parent_frame
        self.current_date = datetime.date.today()
        self.calendar_frame = tk.Frame(self.parent_frame, width=600)
        self.calendar_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        self.draw_calendar()

    def draw_calendar(self):
        for widget in self.calendar_frame.winfo_children():
            widget.destroy()

        #display current month and year
        tk.Label(self.calendar_frame, text=f"{month_name[self.current_date.month]} {self.current_date.year}",
                 font=("Arial", 16)).pack()

        week_days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        tk.Frame(self.calendar_frame, height=5).pack()  #spacer
        days_frame = tk.Frame(self.calendar_frame)
        days_frame.pack()
        for day in week_days:
            tk.Label(days_frame, text=day, width=5, font=("Arial", 12), anchor="center").grid(row=0, column=week_days.index(day))

        #display days of the current month
        days = monthcalendar(self.current_date.year, self.current_date.month)
        for row, week in enumerate(days):
            for col, day in enumerate(week):
                day_label = tk.Label(
                    days_frame, text=f"{day}" if day != 0 else "", width=5, font=("Arial", 12), anchor="center"
                )
                day_label.grid(row=row + 1, column=col)

        #navigation buttons for the calendar
        nav_frame = tk.Frame(self.calendar_frame)
        nav_frame.pack(pady=5)
        tk.Button(nav_frame, text="<<", command=self.previous_month).pack(side="left", padx=5)
        tk.Button(nav_frame, text=">>", command=self.next_month).pack(side="right", padx=5)

    def previous_month(self):
        if self.current_date.month == 1:
            self.current_date = self.current_date.replace(year=self.current_date.year - 1, month=12)
        else:
            self.current_date = self.current_date.replace(month=self.current_date.month - 1)
        self.draw_calendar()

    def next_month(self):
        if self.current_date.month == 12:
            self.current_date = self.current_date.replace(year=self.current_date.year + 1, month=1)
        else:
            self.current_date = self.current_date.replace(month=self.current_date.month + 1)
        self.draw_calendar()
