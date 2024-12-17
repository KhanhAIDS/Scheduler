import tkinter as tk
from tkinter import messagebox
import winsound
import threading


class Notification:
    """
    A class to create a notification window and play a notification sound.
    """
    def __init__(self, event_name: str, event_type: str, event_timeframe: str, text: str):
        """
        Initialize the Notification object.

        :param event_name: Name of the event.
        :param event_type: Type of the event.
        :param event_timeframe: Timeframe for the event.
        :param text: Additional text to display in the notification.
        """
        self.event_name = event_name
        self.event_type = event_type
        self.event_timeframe = event_timeframe
        self.text = text

    def display_notification(self):
        """Display the notification window and play the notification sound."""
        # Play Windows notification sound in a separate thread
        sound_thread = threading.Thread(target=self._play_notification_sound)
        sound_thread.start()

        # Create the notification window
        notification_window = tk.Tk()
        notification_window.title("Event Notification")
        notification_window.geometry("300x150")
        notification_window.resizable(False, False)

        # Add event details to the window
        tk.Label(notification_window, text="Event Notification", font=("Arial", 14, "bold")).pack(pady=5)
        tk.Label(notification_window, text=f"Name: {self.event_name}", anchor="w").pack(pady=2)
        tk.Label(notification_window, text=f"Type: {self.event_type}", anchor="w").pack(pady=2)
        tk.Label(notification_window, text=f"Time: {self.event_timeframe}", anchor="w").pack(pady=2)
        tk.Label(notification_window, text=self.text, wraplength=280, anchor="w").pack(pady=5)

        # Add a dismiss button
        tk.Button(notification_window, text="Dismiss", command=notification_window.destroy).pack(pady=5)

        # Run the notification window
        notification_window.mainloop()

    def _play_notification_sound(self):
        """Play the default Windows notification sound."""
        try:
            print("Playing notification sound...")
            winsound.MessageBeep(winsound.MB_ICONASTERISK)  # Windows default sound
        except Exception as e:
            print(f"Error playing notification sound: {e}")

    def display_notification_details(self):
        """Display notification details."""
        print("Notification Details:")
        print(f"  Event Name: {self.event_name}")
        print(f"  Event Type: {self.event_type}")
        print(f"  Event Timeframe: {self.event_timeframe}")
        print(f"  Message: {self.text}")