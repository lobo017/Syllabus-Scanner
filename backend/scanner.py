import re
from datetime import datetime

def extract_dates_from_syllabus(txt_file_path):
    """
    Extracts important dates and associated descriptions from a syllabus text file.

    Args:
        txt_file_path (str): Path to the .txt file containing syllabus information.

    Returns:
        list[dict]: A list of dictionaries with 'date' and 'context'.
    """
    important_dates = []
    current_year = 2024  # Hardcoded for the Fall 2024 syllabus

    # More comprehensive date pattern
    date_pattern = re.compile(
        r'\b('
        r'\d{1,2}/\d{1,2}(/\d{2,4})?|'           # MM/DD or MM/DD/YYYY
        r'\d{1,2}-\d{1,2}(-\d{2,4})?|'           # MM-DD or MM-DD-YYYY
        r'(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2}'
        r'(?:,\s+\d{4})?'
        r')\b', 
        re.IGNORECASE
    )

    # Read the syllabus text
    with open(txt_file_path, 'r', encoding='utf-8') as f:
        text = f.read()

    # Find dates near academic calendar or important sections
    academic_calendar_section = re.search(r'Academic Calendar(.*?)(?=\n\n|\Z)', text, re.DOTALL | re.IGNORECASE)
    
    if academic_calendar_section:
        calendar_text = academic_calendar_section.group(1)
        
        # Split into lines for more precise parsing
        lines = calendar_text.split('\n')
        
        for line in lines:
            # Check if line contains a date
            date_matches = date_pattern.findall(line)
            
            for date_match in date_matches:
                # Ensure we're using the first element of the potential tuple
                date_str = date_match[0] if isinstance(date_match, tuple) else date_match
                
                parsed_date = parse_date(date_str, current_year)
                
                if parsed_date:
                    # Look for context in the same line
                    context = line.strip()
                    
                    important_dates.append({
                        "date": parsed_date,
                        "context": context
                    })

    return important_dates

def parse_date(date_str, default_year):
    """
    Parses a date string into a standardized format (YYYY-MM-DD).
    """
    date_formats = [
        "%m/%d/%Y", "%m/%d", 
        "%m-%d-%Y", "%m-%d",
        "%B %d, %Y", "%B %d",
        "%b %d, %Y", "%b %d"
    ]

    # Clean and standardize the date string
    date_str = date_str.replace('/', '-').replace(',', '')

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
