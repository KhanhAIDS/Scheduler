import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
import os
import threading
from datetime import datetime
from alarm import Alarm


class alarm_screen:
    def __init__(self, root):
        self.root = root
        self.root.title("Alarm Application")

        # Initialize Alarm instance
        self.alarm = Alarm("", 1)
        self.alarm_time = None
        self.alarm_sound_file_directory = None

        # GUI Elements
        self.label_sound = tk.Label(root, text="Alarm Sound File:")
        self.label_sound.grid(row=0, column=0, padx=10, pady=10)

        self.sound_var = tk.StringVar()
        self.dropdown_sound = ttk.Combobox(root, textvariable=self.sound_var, width=37)
        self.dropdown_sound.grid(row=0, column=1, padx=10, pady=10)
        self.update_sound_list()

        self.button_play = tk.Button(root, text="Play Alarm", command=self.play_alarm)
        self.button_play.grid(row=0, column=2, padx=10, pady=10)

        self.label_repetition = tk.Label(root, text="Repetition:")
        self.label_repetition.grid(row=1, column=0, padx=10, pady=10)

        self.entry_repetition = tk.Entry(root, width=10)
        self.entry_repetition.grid(row=1, column=1, padx=10, pady=10)

        self.label_time = tk.Label(root, text="Set Alarm Time (HH:MM):")
        self.label_time.grid(row=2, column=0, padx=10, pady=10)

        self.entry_time = tk.Entry(root, width=10)
        self.entry_time.grid(row=2, column=1, padx=10, pady=10)

        self.button_set = tk.Button(root, text="Set Alarm", command=self.set_alarm)
        self.button_set.grid(row=3, column=0, padx=10, pady=10)

        self.button_dismiss = tk.Button(root, text="Dismiss Alarm", command=self.dismiss_alarm)
        self.button_dismiss.grid(row=3, column=2, padx=10, pady=10)

        self.button_details = tk.Button(root, text="Show Details", command=self.show_details)
        self.button_details.grid(row=3, column=1, padx=10, pady=10)

    def update_sound_list(self):
        """Populate the dropdown with available sound files in the 'sound' directory."""
        sound_directory = os.path.join(os.path.dirname(__file__), "sound")
        sound_files = [f for f in os.listdir(sound_directory) if f.endswith((".mp3", ".wav", ".ogg"))]
        self.dropdown_sound["values"] = sound_files
        if sound_files:
            self.dropdown_sound.current(0)
            # Automatically update the selected sound path when a file is selected
            self.sound_var.trace_add("write", self.update_selected_sound_path)
            # Set the default sound file
            self.update_selected_sound_path()

    def update_selected_sound_path(self, *args):
        """Update the alarm sound file directory when a new sound is selected."""
        selected_sound = self.sound_var.get()
        if selected_sound:
            self.alarm_sound_file_directory = os.path.join(os.path.dirname(__file__), "sound", selected_sound)


    
    def play_alarm(self):
        """Play the alarm."""
        sound_path = self.alarm_sound_file_directory
        if not sound_path or not os.path.exists(sound_path):
            messagebox.showerror("Error", f"Sound file does not exist: {sound_path}")
            return
        print(f"Playing alarm from: {sound_path}")
        self.alarm.play_alarm(sound_path)


    def set_alarm(self):
        """Set the alarm sound, repetition, and time."""
        sound_file = self.sound_var.get()
        sound_path = os.path.join("sound", sound_file)
        try:
            repetition = int(self.entry_repetition.get())
            self.alarm.modify_alarm_sound(sound_path)
            self.alarm.modify_alarm_repetition(repetition)

            # Set alarm time
            alarm_time_str = self.entry_time.get()
            self.alarm_time = datetime.strptime(alarm_time_str, "%H:%M").time()

            # Start alarm time monitoring
            threading.Thread(target=self.monitor_alarm_time, daemon=True).start()

            messagebox.showinfo("Success", "Alarm settings updated successfully!")
        except ValueError:
            messagebox.showerror("Error", "Invalid input for repetition or time format.")

    def monitor_alarm_time(self):
        """Monitor the current time and trigger the alarm when it matches the set time."""
        while True:
            if self.alarm_time and datetime.now().time().strftime("%H:%M") == self.alarm_time.strftime("%H:%M"):
                self.play_alarm()
                break

    def dismiss_alarm(self):
        """Dismiss the currently playing alarm."""
        self.alarm.dismiss_alarm()

    def show_details(self):
        """Display alarm details in a popup."""
        details = (f"Alarm Details:\n"
                   f"Sound File: {self.alarm_sound_file_directory}\n"
                   f"Repetition: {self.alarm.alarm_repetition}\n"
                   f"Alarm Time: {self.alarm_time.strftime('%H:%M') if self.alarm_time else 'Not Set'}\n"
                   f"Dismissed: {'Yes' if self.alarm.is_dismissed else 'No'}")
        messagebox.showinfo("Alarm Details", details)

if __name__ == "__main__":
    root = tk.Tk()
    app = alarm_screen(root)
    root.mainloop()
