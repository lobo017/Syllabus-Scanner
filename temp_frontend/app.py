import streamlit as st
import requests
import os
import pandas as pd
from datetime import datetime
import icalendar
import sys

# Import custom calendar component
from calendar_component import CalendarComponent

# Import backend processing
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from backend.scanner import extract_dates_from_syllabus

def process_syllabus(uploaded_file):
    """
    Upload syllabus to backend and extract important dates
    """
    # Prepare file for upload
    files = {'file': (uploaded_file.name, uploaded_file, uploaded_file.type)}
    
    try:
        # Upload file to backend
        response = requests.post("http://127.0.0.1:5000/upload", files=files)
        
        # Check if upload was successful
        if response.status_code != 200:
            st.error(f"Upload failed: {response.json().get('error', 'Unknown error')}")
            return []
        
        # Get the parsed file path from the response
        parsed_path = response.json().get('parsed_path')
        
        # Extract dates from the parsed file
        important_dates = extract_dates_from_syllabus(parsed_path)
        
        # Transform dates into a format suitable for the calendar
        formatted_events = [
            {
                "title": date_info.get('context', 'Event'),
                "start_date": datetime.strptime(date_info['date'], "%Y-%m-%d"),
                "description": date_info.get('context', '')
            }
            for date_info in important_dates
            if date_info.get('date')
        ]
        
        return formatted_events
    
    except Exception as e:
        st.error(f"Error processing syllabus: {e}")
        return []

def generate_ical(events):
    """
    Generate an iCal file from events
    """
    cal = icalendar.Calendar()

    for event in events:
        ical_event = icalendar.Event()
        ical_event.add('summary', event['title'])
        ical_event.add('dtstart', event['start_date'])
        ical_event.add('description', event.get('description', ''))
        
        cal.add_component(ical_event)

    return cal.to_ical()

def main():
    # Page configuration
    st.set_page_config(layout="wide", page_title="Syllabus Calendar")

    # Initialize calendar component
    calendar_component = CalendarComponent()

    # Title
    st.title("Syllabus Calendar Importer")

    # Create main columns
    sidebar, main_content = st.columns([1, 3])

    with sidebar:
        # Sidebar Navigation
        st.sidebar.header("Navigation")
        page = st.sidebar.radio("Go to", 
            ["Calendar", "Upcoming Due Dates", "Account Info"]
        )

        # Account Information
        if page == "Account Info":
            st.sidebar.subheader("User Details")
            st.sidebar.write("Email: example@university.edu")
            st.sidebar.write("Semester: Fall 2024")

        # Upcoming Due Dates
        elif page == "Upcoming Due Dates":
            st.sidebar.subheader("Upcoming Assignments")
            # Placeholder for actual due dates
            due_dates = [
                "Midterm Exam - Sep 15, 2024",
                "Final Project - Dec 10, 2024"
            ]
            for date in due_dates:
                st.sidebar.write(f"• {date}")

    with main_content:
        # File uploader for syllabus
        uploaded_file = st.file_uploader("Upload Syllabus", type=['docx', 'pdf'])

        # Initialize events list
        if 'syllabus_events' not in st.session_state:
            st.session_state.syllabus_events = []

        # Process uploaded syllabus
        if uploaded_file:
            # Extract events from syllabus
            events = process_syllabus(uploaded_file)

            if events:
                # Store events in session state
                st.session_state.syllabus_events = events

                # Display events in a table
                events_df = pd.DataFrame(events)
                st.dataframe(events_df[['title', 'start_date']])

                # Download iCal option
                ical_file = generate_ical(events)
                st.download_button(
                    label="Download iCal File",
                    data=ical_file,
                    file_name="syllabus_calendar.ics",
                    mime="text/calendar"
                )

        # Render the calendar with events
        calendar_component.render_calendar(st.session_state.syllabus_events)

if __name__ == "__main__":
    main()