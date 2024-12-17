import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from event import Event
from alarm import Alarm
from notification import Notification


class ConfigureDay:
    def __init__(self, root):
        self.root = root
        self.root.title("Configure Day Events")
        self.event_list = []  # List to store Event objects
        self.selected_event = None  # Currently selected event
        self.setup_ui()

    def setup_ui(self):
        """Set up the main GUI layout."""
        # Frame for Event List
        self.event_frame = tk.Frame(self.root)
        self.event_frame.pack(side="left", fill="y", padx=10, pady=10)

        # Event List Label
        tk.Label(self.event_frame, text="Event List", font=("Arial", 14)).pack(pady=5)
        self.event_listbox = tk.Listbox(self.event_frame, width=40, height=20, font=("Arial", 12))
        self.event_listbox.pack(pady=10)
        self.event_listbox.bind("<<ListboxSelect>>", self.on_event_select)

        # Buttons for Add, Modify, Delete
        button_frame = tk.Frame(self.event_frame)
        button_frame.pack(pady=5)

        tk.Button(button_frame, text="Add Event", font=("Arial", 12), height=2, width=15,
                  command=self.open_event_window).pack(side="left", padx=5)
        tk.Button(button_frame, text="Modify Event", font=("Arial", 12), height=2, width=15,
                  command=self.open_modify_event_window).pack(side="left", padx=5)
        tk.Button(button_frame, text="Delete Event", font=("Arial", 12), height=2, width=15,
                  command=self.delete_event).pack(side="left", padx=5)

        # Frame for Event Details
        self.details_frame = tk.Frame(self.root)
        self.details_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        tk.Label(self.details_frame, text="Event Details", font=("Arial", 14)).pack(pady=5)
        self.details_text = tk.Text(self.details_frame, width=50, height=20, font=("Arial", 12), state="disabled")
        self.details_text.pack()

    def open_event_window(self, event_obj=None):
        """Open a window to add or modify an event."""
        window = tk.Toplevel(self.root)
        window.title("Add/Modify Event")

        # Input Fields
        tk.Label(window, text="Event Name:", font=("Arial", 12)).grid(row=0, column=0, padx=10, pady=5)
        event_name_var = tk.StringVar(value=event_obj.event_name if event_obj else "")
        tk.Entry(window, textvariable=event_name_var, font=("Arial", 12)).grid(row=0, column=1)

        tk.Label(window, text="Event Type:", font=("Arial", 12)).grid(row=1, column=0, padx=10, pady=5)
        event_type_var = tk.StringVar(value=event_obj.event_type if event_obj else "")
        ttk.Combobox(window, textvariable=event_type_var, font=("Arial", 12),
                     values=["Meeting", "Task", "Appointment"]).grid(row=1, column=1)

        tk.Label(window, text="Timeframe (24h):", font=("Arial", 12)).grid(row=2, column=0, padx=10, pady=5)
        timeframe_var = tk.StringVar(value=event_obj.event_timeframe if event_obj else "")
        ttk.Combobox(window, textvariable=timeframe_var, font=("Arial", 12),
                     values=[f"{h:02d}:00-{h+1:02d}:00" for h in range(24)]).grid(row=2, column=1)

        tk.Label(window, text="Event Note:", font=("Arial", 12)).grid(row=3, column=0, padx=10, pady=5)
        event_note_var = tk.StringVar(value=event_obj.event_note if event_obj else "")
        tk.Entry(window, textvariable=event_note_var, font=("Arial", 12)).grid(row=3, column=1)

        # Allow Reminder
        allow_reminder_var = tk.BooleanVar(value=event_obj.allow_reminder if event_obj else False)
        tk.Checkbutton(window, text="Allow Reminder", font=("Arial", 12), variable=allow_reminder_var,
                       command=lambda: toggle_reminder()).grid(row=4, column=0, columnspan=2, pady=5)
        reminder_type_var = tk.StringVar(value="none")
        # Repeat Option
        tk.Label(window, text="Repeat:", font=("Arial", 12)).grid(row=7, column=0, padx=10, pady=5)
        repeat_count_var = tk.StringVar(value="1")
        repeat_unit_var = tk.StringVar(value="days")
        repeat_frame = tk.Frame(window)
        repeat_frame.grid(row=7, column=1, padx=10, pady=5, sticky="W")
        repeat_count_combobox = ttk.Combobox(repeat_frame, textvariable=repeat_count_var, font=("Arial", 12),
                                              values=[str(i) for i in range(1, 7)])
        repeat_count_combobox.pack(side="left")
        repeat_unit_combobox = ttk.Combobox(repeat_frame, textvariable=repeat_unit_var, font=("Arial", 12),
                                             values=["days", "weeks", "months", "years"])
        repeat_unit_combobox.pack(side="left")
        reminder_type_var = tk.StringVar(value="none")
        alarm_settings = {}
        def toggle_reminder():
            if allow_reminder_var.get():
                # Create reminder settings
                tk.Label(window, text="Reminder Type:", font=("Arial", 12)).grid(row=5, column=0)
                
                reminder_type_box = ttk.Combobox(window, textvariable=reminder_type_var, font=("Arial", 12),
                                                values=["alarm", "notification"])
                reminder_type_box.grid(row=5, column=1)

                def handle_reminder_type_change(event):
                    if reminder_type_var.get() == "alarm":
                        # Select sound file
                        alarm_settings["file"] = filedialog.askopenfilename(title="Select Sound File")
                        alarm_settings["repetition"] = tk.StringVar(value="1")

                        tk.Label(window, text="Repetition:", font=("Arial", 12)).grid(row=6, column=0)
                        ttk.Combobox(window, textvariable=alarm_settings["repetition"],
                                    values=["1", "2", "3", "4", "5"]).grid(row=6, column=1)

        # Liên kết sự kiện thay đổi giá trị
                reminder_type_box.bind("<<ComboboxSelected>>", handle_reminder_type_change)
        # Save Event Functionality
        def save_event():
            event_name=event_name_var.get()
            event_type=event_type_var.get()
            event_timeframe=timeframe_var.get()
            if event_name == "" or event_type == "" or event_timeframe == "": 
                messagebox.showerror("Error", "Please fill name, type and timeframe.")
                return
            # Give error message if input is lack of necessary information
            new_event = Event(
                event_name=event_name_var.get(),
                event_type=event_type_var.get(),
                event_timeframe=timeframe_var.get(),
                allow_reminder=allow_reminder_var.get(),
                event_note=event_note_var.get()
            )

            if allow_reminder_var.get():
                if reminder_type_var.get() == "alarm":
                    new_event.set_reminder(reminder_type="alarm", sound_file=alarm_settings["file"],
                                           repetition=int(alarm_settings["repetition"].get()))
                elif reminder_type_var.get() == "notification":
                    new_event.set_reminder(reminder_type="notification")

            self.event_list.append(new_event)
            self.event_listbox.insert(tk.END, new_event.event_name)
            window.destroy()

        tk.Button(window, text="Save", font=("Arial", 12), command=save_event).grid(row=8, column=0, columnspan=2, pady=10)

    def open_modify_event_window(self):
        """Open the event window to modify an existing event."""
        selection = self.event_listbox.curselection()
        if selection:
            index = selection[0]
            event_obj = self.event_list[index]
            self.open_event_window(event_obj)
            self.delete_event()

    def on_event_select(self, event):
        """Display details of the selected event."""
        selection = self.event_listbox.curselection()
        if selection:
            index = selection[0]
            event_obj = self.event_list[index]
            details = (
                f"Name: {event_obj.event_name}\n"
                f"Type: {event_obj.event_type}\n"
                f"Timeframe: {event_obj.event_timeframe}\n"
                f"Note: {event_obj.event_note}\n"
                f"Reminder: {'Enabled' if event_obj.allow_reminder else 'Disabled'}"
            )
            self.details_text.config(state="normal")
            self.details_text.delete("1.0", tk.END)
            self.details_text.insert(tk.END, details)
            self.details_text.config(state="disabled")

    def delete_event(self):
        """Delete the selected event."""
        selection = self.event_listbox.curselection()
        if selection:
            index = selection[0]
            self.event_list.pop(index)
            self.event_listbox.delete(index)


if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("1000x600")
    app = ConfigureDay(root)
    root.mainloop()
