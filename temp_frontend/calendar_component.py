import streamlit as st
import calendar
from datetime import datetime, timedelta
import pytz

class CalendarComponent:
    def __init__(self):
        # Initialize calendar state
        if 'current_month' not in st.session_state:
            now = datetime.now()
            st.session_state.current_month = now.month
            st.session_state.current_year = now.year

    def _get_calendar_matrix(self, month, year):
        """
        Generate a matrix representation of the calendar
        """
        # Get the first day of the month and its weekday
        first_day = datetime(year, month, 1)
        first_weekday = first_day.weekday()
        
        # Get number of days in the month
        _, days_in_month = calendar.monthrange(year, month)
        
        # Create calendar matrix
        calendar_matrix = [[None for _ in range(7)] for _ in range(6)]
        
        # Fill the matrix
        day_counter = 1
        for week in range(6):
            for weekday in range(7):
                # Skip days before the first day of the month
                if week == 0 and weekday < first_weekday:
                    continue
                
                # Stop when we've filled all days of the month
                if day_counter > days_in_month:
                    break
                
                calendar_matrix[week][weekday] = day_counter
                day_counter += 1
        
        return calendar_matrix

    def render_calendar(self, events=None):
        """
        Render the calendar with optional events
        """
        # Get current month and year from session state
        month = st.session_state.current_month
        year = st.session_state.current_year
        
        # Create calendar navigation
        col1, col2, col3 = st.columns([1,2,1])
        
        with col1:
            if st.button('◀ Previous'):
                # Handle month rollover
                if month == 1:
                    st.session_state.current_month = 12
                    st.session_state.current_year -= 1
                else:
                    st.session_state.current_month -= 1

        with col2:
            st.markdown(f"### {calendar.month_name[month]} {year}")

        with col3:
            if st.button('Next ▶'):
                # Handle month rollover
                if month == 12:
                    st.session_state.current_month = 1
                    st.session_state.current_year += 1
                else:
                    st.session_state.current_month += 1

        # Get calendar matrix
        calendar_matrix = self._get_calendar_matrix(month, year)
        
        # Create calendar grid
        days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        
        # Display days of week
        cols = st.columns(7)
        for i, day in enumerate(days):
            cols[i].markdown(f"**{day}**")
        
        # Display calendar days
        for week in calendar_matrix:
            cols = st.columns(7)
            for i, day in enumerate(week):
                if day is not None:
                    # Check if this day has any events
                    day_events = []
                    if events:
                        day_events = [
                            event for event in events 
                            if event['start_date'].month == month 
                            and event['start_date'].day == day
                        ]
                    
                    # Highlight today's date
                    today = datetime.now()
                    is_today = (day == today.day and month == today.month and year == today.year)
                    
                    # Styling for the day
                    if day_events:
                        # Highlight days with events
                        cols[i].markdown(f"**{day}**")
                        for event in day_events:
                            cols[i].markdown(f"- {event['title']}")
                    elif is_today:
                        # Highlight today with a special style
                        cols[i].markdown(f"**{day}** 🔶")
                    else:
                        cols[i].write(str(day))
                else:
                    cols[i].write('')

    def get_events_for_month(self, events, month, year):
        """
        Filter events for a specific month and year
        """
        return [
            event for event in events 
            if event['start_date'].month == month 
            and event['start_date'].year == year
        ]