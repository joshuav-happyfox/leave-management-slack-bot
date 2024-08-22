from datetime import datetime, timedelta
import calendar

from sqlalchemy import and_, func
from api import fetch_users
from database import session
from models import Leave, ManagerMap, Users

def get_month_ranges(start_date, end_date):
    """
    Given a start_date and end_date, returns:
    - The total duration in days.
    - A list of date ranges spanning from start_date to end_date, considering month boundaries.
    """
    # Parse the input dates
    start_date = datetime.strptime(start_date, "%Y-%m-%d")
    end_date = datetime.strptime(end_date, "%Y-%m-%d")

    # List to hold the ranges
    ranges = []

    current_start_date = start_date

    while current_start_date <= end_date:
        # Find the last day of the current month
        last_day_of_month = calendar.monthrange(current_start_date.year, current_start_date.month)[1]
        month_end_date = datetime(current_start_date.year, current_start_date.month, last_day_of_month)

        # Determine the end date for the current range
        range_end_date = min(month_end_date, end_date)
        
        # Calculate duration and exclude weekends
        duration_days = (range_end_date - current_start_date).days + 1
        weekend_days = 0
        
        current_date = current_start_date
        while current_date <= range_end_date:
            if current_date.weekday() >= 5:  # Saturday or Sunday
                weekend_days += 1
            current_date += timedelta(days=1)
        
        duration_excluding_weekends = duration_days - weekend_days

        # Append the current range to the list
        ranges.append({
            "start_date": current_start_date,
            "end_date": range_end_date,
            "month": current_start_date.month,
            "year": current_start_date.year,
            "duration": duration_excluding_weekends
        })
        

        # Move to the first day of the next month
        if range_end_date < end_date:
            next_month = current_start_date.month + 1 if current_start_date.month < 12 else 1
            next_month_year = current_start_date.year if next_month > 1 else current_start_date.year + 1
            current_start_date = datetime(next_month_year, next_month, 1)
        else:
            break

    return ranges

def tab_menu(options, selected, menu_prefix=""):
    menu = [{
			"type": "actions",
			"elements": [
				{
					"type": "button",
					"text": {
						"type": "plain_text",
						"text": option["text"].title(),
						"emoji": True
					},
                    "style": "primary",
					"value": str(option["value"]),
					"action_id": menu_prefix + option["value"]
				} if option["value"] == selected else {
					"type": "button",
					"text": {
						"type": "plain_text",
						"text": option["text"].title(),
						"emoji": True
					},
					"value": str(option["value"]),
					"action_id": menu_prefix + option["value"]
				} for option in options
			]
    }]
    return menu

def init_admin():
    """
    Initializes the admin user in the database.
    """
    check_admin = session.query(Users).filter_by(is_admin=True).first()
    slack_users = fetch_users()['members']
    slack_user_ids = [ user['id'] for user in slack_users] 
    if not check_admin:
        for user in slack_users:
            if user['is_owner']:
                admin = Users(slack_id=user['id'], is_admin=True, avatar=user['profile']['image_24'], name=user['real_name'])
                session.add(admin)
        print("Admin user added successfully.")
    all_users = { user.slack_id: user for user in session.query(Users).all()}
    for user in slack_users:
        if user['id'] not in all_users:
            session.add(Users(slack_id=user['id'], avatar=user['profile']['image_24'], name=user['real_name']))
        else:
            all_users[user['id']].avatar = user['profile']['image_24']
            all_users[user['id']].name = user['real_name']
    
    for user in all_users:
        if user not in slack_user_ids:
            session.delete(all_users[user])

    session.commit()

def main_header_generate(user_id, default='employee_tab', is_admin=None, is_manager=None):
    options = []
    if is_admin or (is_admin == None and session.query(Users).filter_by(slack_id=user_id, is_admin=True).first()):
        options.append({
            "text": "Admin Mode",
            "value": "admin_tab"
        })
    
    if is_manager or (is_manager == None and session.query(ManagerMap).filter_by(manager_id=user_id).first()):
        options.append({
            "text": "Manager Mode",
            "value": "manager_tab"
        })

    options += [{
        "text": "Employee Mode",
        "value": "employee_tab"
    }]
    return tab_menu(options, default)

def manager_header_generate(default='history_tab'):
    options = [{
        "text": "Leave History",
        "value": "history_tab"
    },{
        "text": "Calendar",
        "value": "calendar_tab"
    }]
    return tab_menu(options, default)

def calculate_leave_balance(user_id, is_intern, emp_view=True):
    """
    Calculate the leave balance for a user.
    
    Args:
        user_id (int): ID of the user whose leave balance is to be calculated.
        is_intern (bool): Indicates if the user is an intern (True) or an employee (False).

    Returns:
        str: Formatted leave balance message.
    """
    now = datetime.now()
    current_month = now.month
    current_year = now.year
    leave_text = ""

    if is_intern:
        # Intern leave balance calculation
        total_duration = session.query(func.sum(Leave.duration)).filter(
            and_(Leave.user_id == user_id, Leave.month == current_month, Leave.year == current_year, Leave.status != 'denied')
        ).scalar() or 0
        max_allowed = 2

        leave_text = f"```\nLeave balance: {max(max_allowed - total_duration,0)} day(s) for this month.\n```"
        if total_duration >= max_allowed:
            if(emp_view): 
                leave_text = f"```\n⚠️ You've exhausted all your leaves for this month. Additional days will cause a reduction in the stipend."
            if total_duration > max_allowed:
                leave_text += f"\n Additional Days Taken + Requested: {total_duration - max_allowed} day(s)"
            leave_text += "\n```"
    else:
        # Employee leave balance calculation
        total_duration = session.query(func.sum(Leave.duration)).filter(
            and_(Leave.user_id == user_id, Leave.year == current_year, Leave.status != 'denied')
        ).scalar() or 0
        max_allowed = 14
        leave_text = f"```\nLeave balance: {max(max_allowed - total_duration, 0)} day(s) for this year.\n```"
        if total_duration >= max_allowed:
            if(emp_view): 
                leave_text = f"```\n⚠️ You've exhausted all your leaves for this year. Additional days will cause a reduction in the salary."
            if total_duration > max_allowed:
                leave_text += f"\n Additional Days Taken + Requested: {total_duration - max_allowed} day(s)"
            leave_text += "\n```"

    return leave_text

def pad_text(text, width):
    lrm = "　"
    total_padding = width - len(text)
    padding = lrm * total_padding
    return f"{padding[:total_padding // 2]}{text}{padding[total_padding // 2:]}"

def event_day_formatter(day):
    if day.startswith("`") and day.endswith("`"):
        return f"`{day[1:-1]:^4}`"
    elif day.endswith("`"):
        return f"{day[:-1]:^4}`"
    elif day.startswith("`"):
        return f"` {day[1:]:^4}"
    elif day.endswith("_"):
        return f"{day[:-1]:^4}"
    else:
        return pad_text(day, 4)
    
def mark_events(day_names, events):
    marked_dates = [str(day.day) for day in day_names]

    for event in events:
        start = event.start_date
        end = event.end_date
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
                elif inside_range:
                    marked_dates[i] = f"{marked_dates[i]}_"
            else:
                if inside_range and not closed:
                    marked_dates[i-1] += "`"
                    inside_range = False

    return " | ".join(event_day_formatter(day) for day in marked_dates) + " |"