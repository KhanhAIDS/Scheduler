import json
from datetime import datetime

class today_schedule:
    #load data
    file_path = './table_data.json'
    with open(file_path, 'r', encoding="utf8") as file:
        schedule_data = json.load(file)

    @staticmethod
    def get_today_schedule():
        """Get today's schedule filtered by both date and weekday."""
        today_date = datetime.now().strftime("%d-%m-%Y")
        today_weekday = datetime.now().strftime("%A")
        return today_schedule.filter_schedule_for_today_by_day(
            today_schedule.schedule_data, today_date, today_weekday
        )

    @staticmethod
    def filter_schedule_for_today_by_day(data, today_date, today_weekday):
        """Filter schedule data by today's date or weekday code."""
        today_schedules = []
        weekday_map = {
            "Monday": "T2",
            "Tuesday": "T3",
            "Wednesday": "T4",
            "Thursday": "T5",
            "Friday": "T6",
            "Saturday": "T7",
            "Sunday": "CN"
        }

        weekday_code = weekday_map.get(today_weekday, "")
        for entry in data:
            value5 = entry.get("Value5", "")

            #check if the specific date or weekday code is mentioned
            if today_date in value5 or weekday_code in value5:
                today_schedules.append({
                    "Value2": entry.get("Value2", ""),
                    "Value5":entry.get("Value5", "").split(",")[2].strip() if "," in value5 else "",
                    "Value7": entry.get("Value7", "")
                })
        return today_schedules
