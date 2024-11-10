import re
from datetime import datetime, timedelta
from dateutil import parser
from dateutil.rrule import rrule, WEEKLY
import pytz
from icalendar import Calendar, Event
import spacy
from pathlib import Path
import logging

class SyllabusProcessor:
    def __init__(self):
        # Initialize spaCy for NLP
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except OSError:
            # If model isn't installed, download it
            import subprocess
            subprocess.run(["python", "-m", "spacy", "download", "en_core_web_sm"])
            self.nlp = spacy.load("en_core_web_sm")
        
        # Common date patterns in syllabi
        self.date_patterns = [
            # Standard date formats
            r"(jan(?:uary)?|feb(?:ruary)?|mar(?:ch)?|apr(?:il)?|may|jun(?:e)?|"
            r"jul(?:y)?|aug(?:ust)?|sep(?:tember)?|oct(?:ober)?|nov(?:ember)?|"
            r"dec(?:ember)?)\s+\d{1,2}(?:st|nd|rd|th)?,?\s+\d{4}",
            
            # MM/DD/YYYY or MM-DD-YYYY
            r"\d{1,2}[-/]\d{1,2}[-/]\d{4}",
            
            # Week references
            r"week\s+\d{1,2}",
            
            # Recurring patterns
            r"every\s+(monday|tuesday|wednesday|thursday|friday|saturday|sunday)",
            
            # Date ranges
            r"(jan(?:uary)?|feb(?:ruary)?|mar(?:ch)?|apr(?:il)?|may|jun(?:e)?|"
            r"jul(?:y)?|aug(?:ust)?|sep(?:tember)?|oct(?:ober)?|nov(?:ember)?|"
            r"dec(?:ember)?)\s+\d{1,2}(?:st|nd|rd|th)?\s*[-–]\s*\d{1,2}(?:st|nd|rd|th)?,?\s+\d{4}"
        ]
        
        # Initialize logger
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

    def extract_dates(self, text):
        """Extract dates and associated events from syllabus text."""
        events = []
        doc = self.nlp(text)
        
        # Process text line by line
        for line in text.split('\n'):
            if not line.strip():
                continue
                
            # Look for dates using patterns
            date_found = False
            for pattern in self.date_patterns:
                matches = re.finditer(pattern, line.lower())
                for match in matches:
                    date_str = match.group()
                    try:
                        # Extract date and associated text
                        date = self._parse_date(date_str)
                        if date:
                            # Get the event description (text after the date)
                            description = line[match.end():].strip()
                            if not description:
                                # If no text after date, use previous text
                                description = line[:match.start()].strip()
                            
                            events.append({
                                'date': date,
                                'description': description,
                                'original_text': line.strip()
                            })
                            date_found = True
                    except ValueError as e:
                        self.logger.warning(f"Could not parse date '{date_str}': {e}")
            
            # If no explicit date found, look for temporal references
            if not date_found:
                temporal_refs = self._extract_temporal_references(line)
                events.extend(temporal_refs)
        
        return events

    def _parse_date(self, date_str):
        """Parse various date formats into datetime objects."""
        try:
            # Handle "Week X" format
            if 'week' in date_str.lower():
                week_num = int(re.search(r'\d+', date_str).group())
                # Assuming the semester starts on the first Monday of January
                base_date = datetime(datetime.now().year, 1, 1)
                while base_date.weekday() != 0:  # 0 is Monday
                    base_date += timedelta(days=1)
                return base_date + timedelta(weeks=week_num-1)
            
            # Handle recurring days
            if 'every' in date_str.lower():
                day_match = re.search(r'(monday|tuesday|wednesday|thursday|friday|saturday|sunday)', date_str.lower())
                if day_match:
                    day_name = day_match.group(1)
                    days = {'monday': 0, 'tuesday': 1, 'wednesday': 2, 
                           'thursday': 3, 'friday': 4, 'saturday': 5, 'sunday': 6}
                    return {'type': 'recurring', 'weekday': days[day_name]}
            
            # Try parsing with dateutil
            return parser.parse(date_str, fuzzy=True)
            
        except ValueError:
            self.logger.warning(f"Failed to parse date: {date_str}")
            return None

    def _extract_temporal_references(self, text):
        """Extract temporal references that might indicate dates."""
        events = []
        doc = self.nlp(text)
        
        # Look for temporal entities
        for ent in doc.ents:
            if ent.label_ in ['DATE', 'TIME']:
                try:
                    date = dateutil.parser.parse(ent.text, fuzzy=True)
                    events.append({
                        'date': date,
                        'description': text.replace(ent.text, '').strip(),
                        'original_text': text.strip()
                    })
                except ValueError:
                    continue
                    
        return events

    def create_calendar(self, events, course_info=None, timezone='UTC'):
        """Create an iCalendar file from extracted events."""
        cal = Calendar()
        cal.add('prodid', '-//Syllabus Calendar Generator//EN')
        cal.add('version', '2.0')
        
        tz = pytz.timezone(timezone)
        
        for event_data in events:
            event = Event()
            
            if isinstance(event_data['date'], dict) and event_data['date']['type'] == 'recurring':
                # Handle recurring events
                start_date = datetime.now().replace(hour=9, minute=0, second=0, microsecond=0)
                end_date = start_date.replace(month=12, day=31)  # End of year
                
                # Create recurring rule
                rule = rrule(
                    freq=WEEKLY,
                    dtstart=start_date,
                    until=end_date,
                    byweekday=event_data['date']['weekday']
                )
                
                # Add recurrence rule to event
                event.add('rrule', {'freq': 'WEEKLY', 'until': end_date})
                event_date = start_date
            else:
                event_date = event_data['date']
            
            # Set default time to 9 AM if no time specified
            if event_date.hour == 0:
                event_date = event_date.replace(hour=9)
            
            event_date = tz.localize(event_date)
            
            event.add('dtstart', event_date)
            event.add('dtend', event_date + timedelta(hours=1))
            event.add('summary', event_data['description'])
            
            if course_info:
                event.add('description', (
                    f"Course: {course_info.get('title', 'N/A')}\n"
                    f"Instructor: {course_info.get('instructor', 'N/A')}\n\n"
                    f"Original text: {event_data['original_text']}"
                ))
            
            cal.add_component(event)
        
        return cal

    def process_syllabus(self, syllabus_text, course_info=None, timezone='UTC'):
        """Process syllabus and create iCalendar file."""
        try:
            # Extract dates and events
            events = self.extract_dates(syllabus_text)
            
            if not events:
                raise ValueError("No dates found in the syllabus text")
            
            # Create calendar
            calendar = self.create_calendar(events, course_info, timezone)
            
            return calendar
            
        except Exception as e:
            self.logger.error(f"Error processing syllabus: {str(e)}")
            raise

def main():
    # Example usage
    processor = SyllabusProcessor()
    
    # Sample syllabus text
    syllabus_text = """
    Introduction to Python Programming
    Spring 2024
    
    Week 1 - Introduction to Python basics
    January 15, 2024 - Variables and Data Types
    Every Tuesday - Lab Sessions
    Jan 22 - Control Flow
    Week 3 - Functions and Modules
    """
    
    course_info = {
        'title': 'Introduction to Python Programming',
        'instructor': 'Dr. Smith'
    }
    
    try:
        calendar = processor.process_syllabus(
            syllabus_text,
            course_info=course_info,
            timezone='America/New_York'
        )
        
        # Save the calendar
        with open('syllabus_calendar.ics', 'wb') as f:
            f.write(calendar.to_ical())
            
        print("Calendar created successfully!")
        
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()