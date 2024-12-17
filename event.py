from alarm import Alarm
from notification import Notification

class Event:
    """
    A class to represent an event with attributes for type, name, timeframe, 
    notes, reminders, and methods to modify these attributes.
    """
    def __init__(
        self,
        event_type: str,
        event_name: str,
        event_timeframe: str,
        allow_reminder: bool = False,
        event_note: str = ""
    ):
        """
        Initialize the Event object.

        :param event_type: Type/category of the event.
        :param event_name: Name/description of the event.
        :param event_timeframe: The time range for the event.
        :param allow_reminder: Boolean to specify if reminders are enabled.
        :param event_note: Custom note for the event.
        """
        self.event_type = event_type
        self.event_name = event_name
        self.event_timeframe = event_timeframe
        self.allow_reminder = allow_reminder
        self.event_note = event_note  # New attribute for custom notes
        self.reminder = None  # Holds the Alarm or Notification instance

    def modify_event_type(self, new_event_type: str):
        """Modify the event type."""
        self.event_type = new_event_type

    def modify_event_name(self, new_event_name: str):
        """Modify the event name."""
        self.event_name = new_event_name

    def modify_event_timeframe(self, new_timeframe: str):
        """Modify the event timeframe."""
        self.event_timeframe = new_timeframe

    def modify_event_note(self, new_event_note: str):
        """Modify the custom event note."""
        self.event_note = new_event_note

    def set_reminder(self, reminder_type: str, **kwargs):
        """
        Set a reminder for the event: either 'alarm' or 'notification'.
        :param reminder_type: Type of reminder ('alarm' or 'notification').
        :param kwargs: Additional arguments for alarm or notification.
        """
        if not self.allow_reminder:
            print("Reminders are not allowed for this event.")
            return

        if reminder_type == "alarm":
            sound_file = kwargs.get("sound_file")
            repetition = kwargs.get("repetition", 1)
            self.reminder = Alarm(alarm_sound_file_directory=sound_file, alarm_repetition=repetition)
            print("Alarm reminder set successfully.")
        elif reminder_type == "notification":
            self.reminder = Notification(
                event_name=self.event_name,
                event_type=self.event_type,
                event_timeframe=self.event_timeframe,
                text=self.event_note
            )
            print("Notification reminder set successfully.")
        else:
            print("Invalid reminder type. Choose 'alarm' or 'notification'.")

    def display_event_details(self):
        """Display event details."""
        print(f"Event: {self.event_name}")
        print(f"Type: {self.event_type}")
        print(f"Timeframe: {self.event_timeframe}")
        print(f"Note: {self.event_note}")
        print(f"Reminder: {'Enabled' if self.allow_reminder else 'Disabled'}")
        if self.reminder:
            print(f"Reminder Type: {type(self.reminder).__name__}")