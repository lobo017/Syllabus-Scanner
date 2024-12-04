import re
from datetime import datetime
import logging
from typing import List, Dict

def extract_dates_from_syllabus(file_path: str) -> List[Dict[str, str]]:
    """
    Extract important dates and events from the syllabus
    
    Args:
        file_path (str): Path to the text file containing syllabus content
    
    Returns:
        List of dictionaries containing date information
    """
    # Configure logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    try:
        # Read the text file
        with open(file_path, 'r', encoding='utf-8') as f:
            syllabus_text = f.read()

        # Date extraction patterns
        important_dates = []

        # Pattern for dates in specific formats
        date_patterns = [
            # Month Day, Year format
            r'\b(January|February|March|April|May|June|July|August|September|October|November|December)\s+(\d{1,2}),\s+(\d{4})\b',
            # Month/Day/Year format
            r'\b(\d{1,2}/\d{1,2}/\d{4})\b'
        ]

        # Specific date contexts to look for
        date_contexts = [
            r'Course Start',
            r'Midterm Project',
            r'Fall Break',
            r'Final Presentations',
            r'Final Project',
            r'Lab \d+',
            r'Week \d+',
            r'Office Hours'
        ]

        # Extract dates with their contexts
        for pattern in date_patterns:
            matches = re.finditer(pattern, syllabus_text)
            for match in matches:
                # Find nearby context
                start = max(0, match.start() - 100)
                end = min(len(syllabus_text), match.end() + 100)
                context_area = syllabus_text[start:end]
                
                # Check if the date is near any of the specific contexts
                for context_pattern in date_contexts:
                    context_match = re.search(context_pattern, context_area, re.IGNORECASE)
                    if context_match:
                        important_dates.append({
                            'date': match.group(0),
                            'context': context_match.group(0)
                        })

        # Additional specific date extraction for academic calendar
        calendar_pattern = r'(\d+/\d+)\s+(.+?)\s+(Lab \d+:.+)'
        calendar_matches = re.finditer(calendar_pattern, syllabus_text, re.MULTILINE)
        for match in calendar_matches:
            important_dates.append({
                'date': match.group(1),
                'context': f"{match.group(2)} - {match.group(3)}"
            })

        # Remove duplicates
        unique_dates = []
        seen = set()
        for date_info in important_dates:
            key = (date_info['date'], date_info['context'])
            if key not in seen:
                unique_dates.append(date_info)
                seen.add(key)

        return unique_dates

    except Exception as e:
        logger.error(f"Error extracting dates: {e}")
        return []

def parse_date(date_str, default_year):
    """
    Parses a date string into a standardized format (YYYY-MM-DD).
    
    Args:
        date_str (str): Date string to parse
        default_year (int): Year to use if not specified in date_str
    
    Returns:
        str: Parsed date in YYYY-MM-DD format or None if parsing fails
    """
    # Date formats to try
    date_formats = [
        "%m/%d/%Y", "%m/%d", 
        "%m-%d-%Y", "%m-%d",
        "%B %d, %Y", "%B %d",
        "%b %d, %Y", "%b %d"
    ]

    # Clean and standardize the date string
    date_str = (date_str.replace('/', '-')
                        .replace(',', '')
                        .strip())

    for fmt in date_formats:
        try:
            # If year is missing, use default year
            if '%Y' not in fmt:
                if '/' in date_str or '-' in date_str:
                    date_str = f"{date_str}-{default_year}"
                else:
                    date_str = f"{date_str} {default_year}"
            
            # Parse the date
            parsed_date = datetime.strptime(date_str, fmt)
            return parsed_date.strftime("%Y-%m-%d")
        except ValueError:
            continue
    
    return None