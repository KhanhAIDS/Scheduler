import json
from datetime import datetime, timedelta
from event import Event

class TimetableManager:
    def __init__(self):
        self.timetable_data = []
        self.semester_events = []

    def load_timetable(self, json_file):
        """Load timetable data from JSON file"""
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                self.timetable_data = json.load(f)
            return True
        except Exception as e:
            print(f"Error loading timetable: {e}")
            return False

    def _parse_course_info(self, course):
        """Parse course information from the complex Value5 string"""
        try:
            info = course['Value5']
            parts = info.split(',')
            
            # Get weekday and time
            day_info = parts[0].strip()  # "Sáng T5" or similar
            for part in parts[0].split():
                if part.startswith('T') or part == 'CN':
                    weekday = part
                    break
            
            # Get time range
            time_info = None
            room = None
            weeks = []
            
            for part in parts:
                part = part.strip()
                if 'Từ' in part:  # Format: "Từ 9h15-11h45"
                    time_range = part.replace("Từ ", "")
                elif 'Tiết' in part:  # Format: "Tiết 4-6"
                    period_range = part.replace("Tiết ", "")
                    time_range = self._convert_period_to_time(period_range)
                elif part.startswith('B') or part.startswith('D'):  # Room number
                    room = part
                elif 'Tuần:' in part or 'Tuần' in part:  # Week information
                    week_part = part.replace("Tuần:", "").replace("Tuần", "").strip()
                    if '-' in week_part:  # Range of weeks
                        start, end = map(int, week_part.split('-'))
                        weeks = list(range(start, end + 1))
                    else:  # List of specific weeks
                        weeks = [int(w.strip()) for w in week_part.split(',') if w.strip().isdigit()]
            
            return {
                'weekday': weekday,
                'time_range': time_range,
                'room': room,
                'weeks': weeks
            }
        except Exception as e:
            print(f"Error parsing course info: {e}")
            return None

    def _convert_period_to_time(self, period_range):
        """Convert period numbers to time range (e.g., '4-6' -> '09:55-12:35')"""
        period_times = {
            1: '07:00', 2: '07:55', 3: '08:50', 4: '09:55',
            5: '10:50', 6: '11:45', 7: '12:55', 8: '13:50',
            9: '14:45', 10: '15:50', 11: '16:45', 12: '17:40'
        }
        
        try:
            start, end = map(int, period_range.split('-'))
            return f"{period_times[start]}-{period_times[end]}"
        except:
            return None

    def _parse_weekday(self, weekday_str):
        """Parse weekday from format T2-CN"""
        weekday_map = {'T2': 0, 'T3': 1, 'T4': 2, 'T5': 3, 'T6': 4, 'T7': 5, 'CN': 6}
        return weekday_map.get(weekday_str, -1)

    def _parse_time_range(self, time_str):
        """Parse time range from various formats"""
        if not time_str:
            return None
            
        try:
            if 'h' in time_str:  # Format: "9h15-11h45"
                start, end = time_str.split('-')
                
                def convert_time(t):
                    hour, minute = t.split('h')
                    return f"{int(hour):02d}:{minute}"
                
                return (convert_time(start.strip()), convert_time(end.strip()))
            else:  # Already in "HH:MM-HH:MM" format
                start, end = time_str.split('-')
                return (start.strip(), end.strip())
        except:
            return None

    def generate_semester_events(self, start_date, end_date):
        """Generate recurring events for the entire semester"""
        self.semester_events = []
        start = datetime.strptime(start_date, "%Y-%m-%d")
        
        print("\nGenerating semester events:")
        
        for course in self.timetable_data:
            print(f"\nProcessing course: {course['Value2']}")
            
            course_info = self._parse_course_info(course)
            if not course_info:
                print("Failed to parse course info")
                continue
                
            print(f"Parsed course info: {course_info}")
            
            weekday = self._parse_weekday(course_info['weekday'])
            time_range = self._parse_time_range(course_info['time_range'])
            
            if weekday == -1 or not time_range:
                print(f"Invalid weekday or time range")
                continue
                
            # Create events for specified weeks
            for week in course_info['weeks']:
                # Calculate date for this week
                course_date = start + timedelta(weeks=week-1, days=weekday)
                event_date = course_date.strftime("%Y-%m-%d")
                event_timeframe = f"{event_date} {time_range[0]}-{time_range[1]}"
                
                event = Event(
                    event_type="Class",
                    event_name=course['Value2'],  # Course name
                    event_timeframe=event_timeframe,
                    event_note=f"Room: {course_info['room']}\nTeacher: {course.get('Value7', 'N/A')}",
                    allow_reminder=True
                )
                
                self.semester_events.append(event)
                print(f"Created event for {event_date}")

        print(f"\nTotal events generated: {len(self.semester_events)}")
        return True

    def get_events_for_date(self, date_str):
        """Get all events for a specific date"""
        events = []
        target_date = datetime.strptime(date_str, "%Y-%m-%d")
        
        for event in self.semester_events:
            event_date = datetime.strptime(event.event_timeframe.split()[0], "%Y-%m-%d")
            if event_date.date() == target_date.date():
                events.append(event)
                
        return events

    def get_all_events(self):
        """Return all semester events"""
        return self.semester_events

    def clear_events(self):
        """Clear all semester events"""
        self.semester_events = []
