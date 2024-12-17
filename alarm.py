import threading
from pydub import AudioSegment
from pydub.playback import play
import time
import os
from playsound import playsound
import multiprocessing
class Alarm:
    """
    A class to represent an alarm with sound file, repetition settings, and dismiss functionality.
    """
    def __init__(self, alarm_sound_file_directory: str, alarm_repetition: int = 1):
        """
        Initialize the Alarm object.

        :param alarm_sound_file_directory: Path to the alarm sound file.
        :param alarm_repetition: Number of times the alarm repeats.
        """
        self.alarm_sound_file_directory = alarm_sound_file_directory
        self.alarm_repetition = alarm_repetition
        self.is_dismissed = False
        self.alarm_thread = None

    def modify_alarm_sound(self, new_sound_directory: str):
        """Modify the alarm sound file directory."""
        if os.path.exists(new_sound_directory):
            self.alarm_sound_file_directory = new_sound_directory
            print(f"Alarm sound updated to: {self.alarm_sound_file_directory}")
        else:
            print("Error: Sound file directory does not exist.")

    def modify_alarm_repetition(self, new_repetition: int):
        """Modify the alarm repetition count."""
        if new_repetition > 0:
            self.alarm_repetition = new_repetition
            print(f"Alarm repetition updated to: {self.alarm_repetition}")
        else:
            print("Repetition count must be greater than 0.")

    def dismiss_alarm(self):
        """Dismiss the alarm."""
        self.is_dismissed = True
        print("Alarm has been dismissed.")

    def play_alarm(self, sound_path):
        """Play the alarm sound using the provided path."""
        print(f"Playing sound from {sound_path}")
        playsound(sound_path)
        self.is_dismissed = False
        self.alarm_thread = threading.Thread(target=self._play_alarm_thread)
        self.alarm_thread.start()

    def _play_alarm_thread(self):
        """Internal method to play the alarm sound."""
        print("Playing alarm...")
        for _ in range(self.alarm_repetition):
            if self.is_dismissed:
                print("Alarm stopped.")
                break
            try:
                sound = AudioSegment.from_file(self.alarm_sound_file_directory)
                play(sound)
            except Exception as e:
                print(f"Error playing sound: {e}")
                break
            time.sleep(1)  # Delay between repetitions
        else:
            print("Alarm finished playing.")

    def display_alarm_details(self):
        """Display the current alarm details."""
        print("Alarm Details:")
        print(f"  Sound File: {self.alarm_sound_file_directory}")
        print(f"  Repetition: {self.alarm_repetition} times")
        print(f"  Dismissed: {'Yes' if self.is_dismissed else 'No'}")