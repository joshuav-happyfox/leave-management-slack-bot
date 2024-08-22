from datetime import datetime, timedelta

# Define the week
now = datetime.now()
start_of_week = now - timedelta(days=now.weekday())
days_of_week = [start_of_week + timedelta(days=i) for i in range(7)]

# Example events
events = [
    {"start": 19, "end": 21},
    {"start": 22, "end": 22},
    {"start": 23, "end": 26}
]

# Prepare the day names for formatting
day_names = [day.day for day in days_of_week]

# Function to mark events in the week row
def mark_events(day_names, events):
    # Create a list of empty strings to hold the marked dates
    marked_dates = [day.day for day in day_names]
    
    # Iterate through events to mark ranges
    for event in events:
        start = event["start_date"]
        end = event["end_date"]
        inside_range = False
        closed = False
        for i in range(7):
            if start <= day_names[i] <= end:
                if not inside_range:
                    marked_dates[i] = f"`{marked_dates[i]}"
                    inside_range = True
                elif day_names[i] == end or i == 6:
                    marked_dates[i] = f"{marked_dates[i]}`"
                    closed = True
            else:
                if inside_range and not closed:
                    # Close the range if it was open
                    marked_dates[i-1] += "`"
                    inside_range = False

    # Join marked dates into a row
    return " | ".join(marked_dates)

# Generate the marked dates row
dates_row = mark_events(day_names, events)

print(dates_row)