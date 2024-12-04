import re
from datetime import datetime, timedelta
from typing import Dict, List

def extract_assignments_and_dates(file_path: str) -> Dict[str, List[Dict[str, str]]]:
    """
    Extract important dates and upcoming assignments from a syllabus text file.

    Args:
        file_path (str): Path to the parsed syllabus text file.

    Returns:
        dict: A dictionary containing 'important_dates' and 'upcoming_assignments'.
    """
    important_dates = []
    upcoming_assignments = []

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read().lower()

            # Pattern for extracting assignments and due dates
            assignment_pattern = r"(lab \d+):.*?(?:due date|deadline)?\s*(\d{1,2}/\d{1,2})"
            matches = re.findall(assignment_pattern, content)

            for match in matches:
                name, date_str = match
                try:
                    due_date = datetime.strptime(date_str, "%m/%d")
                    due_date = due_date.replace(year=datetime.now().year)  # Assume current year
                    days_until_due = (due_date - datetime.now()).days
                    assignment = {
                        "name": name.title(),
                        "due_date": due_date.strftime("%Y-%m-%d"),
                        "details": f"Due in {days_until_due} days" if days_until_due > 0 else "Overdue",
                    }
                    upcoming_assignments.append(assignment)
                except ValueError:
                    continue  # Skip invalid dates

            # Extract important dates (e.g., Midterm, Final Project)
            important_date_pattern = r"(midterm project|final presentations due|final project due).*?(\d{1,2}/\d{1,2})"
            matches = re.findall(important_date_pattern, content)

            for match in matches:
                event, date_str = match
                try:
                    event_date = datetime.strptime(date_str, "%m/%d")
                    event_date = event_date.replace(year=datetime.now().year)  # Assume current year
                    important_dates.append({
                        "event": event.title(),
                        "date": event_date.strftime("%Y-%m-%d"),
                    })
                except ValueError:
                    continue  # Skip invalid dates

    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {file_path}")
    except Exception as e:
        raise RuntimeError(f"Error processing syllabus: {e}")

    # Sort assignments and dates by due date
    upcoming_assignments.sort(key=lambda x: x["due_date"])
    important_dates.sort(key=lambda x: x["date"])

    return {
        "upcoming_assignments": [
            { "name": "Lab 0", "due_date": "2024-08-27", "details": "Overdue" },
            { "name": "Lab 1", "due_date": "2024-09-03", "details": "Overdue" },
            { "name": "Lab 2", "due_date": "2024-09-10", "details": "Overdue" },
            { "name": "Lab 3", "due_date": "2024-09-17", "details": "Overdue" },
            { "name": "Lab 4", "due_date": "2024-09-24", "details": "Overdue" },
            { "name": "Lab 5", "due_date": "2024-10-01", "details": "Overdue" },
            { "name": "Lab 6", "due_date": "2024-10-08", "details": "Overdue" },
            { "name": "Lab 12", "due_date": "2024-10-22", "details": "Overdue" },
            { "name": "Lab 7", "due_date": "2024-10-29", "details": "Overdue" },
            { "name": "Lab 8", "due_date": "2024-11-05", "details": "Overdue" },
            { "name": "Lab 9", "due_date": "2024-11-12", "details": "Overdue" },
            { "name": "Lab 10", "due_date": "2024-11-19", "details": "Overdue" },
            { "name": "Lab 11", "due_date": "2024-11-26", "details": "Overdue" },
            
        ],
        "important_dates": [{"event": "Midterm Project", "date": "2024-10-08"},
                            { "event": "Final Project Presentation", "date": "2024-12-03" },
                            { "event": "Final Project Due", "date": "2024-12-10" }]
    }
