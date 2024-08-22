from datetime import datetime, timedelta
from sqlalchemy import and_, or_, select
from database import session
from models import Leave, ManagerMap, Users
from util import mark_events, pad_text

status = {
    'pending': "🟡",
    'accepted': "🟢",
    'denied': "🔴"
}

def displayDelete(leave):
    if leave.status == 'denied':
        return False
    elif leave.status == 'accepted' and leave.start_date <= datetime.now().date():
        return False
    return True

def generate(user=None, manager_filter="view_all", intern_filter=None):
    additional = [
        {
            "type": "section",
            "text": {
            "type": "mrkdwn",
            "text": "An overview of the current week:"
            }
        }
    ]
    leaves = session.query(Leave).all() if not intern_filter else session.query(Leave).filter_by(user_id=intern_filter).all()
    leaves.reverse()
    
    stmt = select(Users
            ).join(ManagerMap, Users.slack_id == ManagerMap.employee_id
            ).where(ManagerMap.manager_id == user)
    
    employees = session.execute(stmt).scalars()
    
    # Get the current date
    now = datetime.now()
    # Find the start of the week (Monday)
    start_of_week = now - timedelta(days=now.weekday())
    # Find the end of the week (Sunday)
    end_of_week = start_of_week + timedelta(days=6)
    # Print the start and end dates
    days_of_week = [(start_of_week + timedelta(days=i)).date() for i in range(7)]
    day_names = ["Mo", "Tu", "We", "Th", "Fr", "Sa", "Su"]

    # Prepare the table headers and dates row
    headers = f"|　　{f"{start_of_week.day}/{start_of_week.month} - {end_of_week.day}/{end_of_week.month}":16} | " + " | ".join(pad_text(day,4) for day in day_names) + " |"
    
    additional += [{
        "type": "context",
        "elements": [
            {
                "type": "mrkdwn",
                "text": f"{'─'*(len(headers)-20)}\n{headers}\n{'─'*(len(headers)-20)}"
            }
        ]
    }]
    
    for employee in employees:
        existing_leaves = session.query(Leave).filter(
            and_(
                Leave.user_id == employee.slack_id, 
                Leave.status != "denied",
                or_(
                    and_(
                        Leave.start_date >= start_of_week,
                        Leave.start_date <= end_of_week
                    ),
                    and_(
                        Leave.end_date >= start_of_week,
                        Leave.end_date <= end_of_week
                    )
                )
        )).all()
        dates_row = mark_events(days_of_week, existing_leaves)
        additional.append({
			"type": "context",
			"elements": [{
					"type": "mrkdwn",
					"text": f"| "
				},
				{
					"type": "image",
					"image_url": employee.avatar,
					"alt_text": "cute cat"
				},
				{
					"type": "mrkdwn",
					"text": f"  {employee.name:15} | {dates_row}"
				}
			]
		})
    additional += [{
        "type": "context",
        "elements": [
            {
                "type": "mrkdwn",
                "text": f"{'─'*(len(headers)-20)}"
            }
        ]
    }]
        
    
    return additional