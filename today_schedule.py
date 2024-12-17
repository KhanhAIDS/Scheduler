import json
from datetime import datetime
import re  # For regex processing


class today_schedule:
    # Load data
    file_path = './table_data.json'
    with open(file_path, 'r', encoding="utf8") as file:
        schedule_data = json.load(file)

    @staticmethod
    def get_today_schedule():
        """Get today's schedule filtered by both date and weekday."""
        today_date = datetime.now().strftime("%d-%m-%Y")
        today_weekday = datetime.now().strftime("%A")
        today_schedules = today_schedule.filter_schedule_for_today_by_day(
            today_schedule.schedule_data, today_date, today_weekday
        )
        today_schedule.save_to_file(today_schedules)  # Save results to a file
        return today_schedules

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
            if today_date in value5 or weekday_code in value5:
                parsed_data = today_schedule.parse_schedule_entry(entry)
                today_schedules.append(parsed_data)

        return today_schedules

    @staticmethod
    def parse_schedule_entry(entry):
        """Parse an individual schedule entry into the desired format."""
        result = {}

        # Parse Value2: Class details
        value2 = entry.get("Value2", "")
        class_details = value2.split("\n")
        result["Tên lớp học"] = class_details[0] if len(class_details) > 0 else "N/A"

        # Extract Class Code and Course Code
        class_code_match = re.search(r"(\d+)", value2)
        result["Mã lớp"] = class_code_match.group(1) if class_code_match else "N/A"

        course_code_match = re.search(r"-\s*(\w+)\s*\(", value2)
        result["Mã môn học"] = course_code_match.group(1) if course_code_match else "N/A"

        # Extract Class Type
        class_type_match = re.search(r"\((.*?)\)", value2)
        if class_type_match:
            class_types = re.split(r"[,+]", class_type_match.group(1))  # Split by "+" or ","
            type_translation = {
                "TN": "Thí nghiệm",
                "LT": "Lý thuyết",
                "BT": "Bài tập",
                "TT": "Thực tập",
                "DA": "Đồ án"
            }
            translated_types = [type_translation.get(t.strip(), t.strip()) for t in class_types]
            result["Loại hình lớp"] = ", ".join(translated_types)
        else:
            result["Loại hình lớp"] = "N/A"

        # Parse Value3: Class format
        value3 = entry.get("Value3", "")
        result["Loại lớp học"] = value3 if value3 else "N/A"

        # Parse Value4: Teams code
        value4 = entry.get("Value4", "")
        result["Mã teams"] = value4 if value4 else "Không có"

        # Parse Value5: Schedule details
        value5 = entry.get("Value5", "")
        value5_parts = value5.split(",")

        result["Ngày học"] = value5_parts[0].strip() if len(value5_parts) > 0 else "N/A"

        # Extract Weekday from "Ngày học"
        weekday_match = re.search(r"T[2-7]|CN", result["Ngày học"])
        result["Thứ"] = weekday_match.group(0) if weekday_match else "N/A"

        result["Giờ học"] = value5_parts[1].strip() if len(value5_parts) > 1 else "N/A"
        result["Địa điểm học"] = value5_parts[2].strip() if len(value5_parts) > 2 else "N/A"

        # Extract Tuần
        week_match = re.search(r"Tuần:\s*(.*?),\s*Kỳ", value5)
        result["Tuần"] = week_match.group(1) if week_match else "N/A"

        # Extract Học kỳ
        semester_match = re.search(r"Kỳ ([A-Za-z]+)", value5)
        result["Học kỳ"] = semester_match.group(1) if semester_match else "N/A"

        # Parse Value7: Lecturer/Assistants
        value7 = entry.get("Value7", "")
        lecturers = value7.split("\n")
        result["Giảng viên"] = ", ".join(lecturers)

        return result

    @staticmethod
    def save_to_file(data, output_file='output_today_schedule.json'):
        """Save the parsed schedule data to a file."""
        with open(output_file, 'w', encoding='utf8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
        print(f"Today's schedule has been saved to {output_file}.")

if __name__ == "__main__":
    today_schedules = today_schedule.get_today_schedule()

    if today_schedules:
        print("Today's Schedule:")
        for idx, schedule in enumerate(today_schedules, start=1):
            print(f"\nEvent {idx}:")
            for key, value in schedule.items():
                print(f"  {key}: {value}")
    else:
        print("No schedule for today.")