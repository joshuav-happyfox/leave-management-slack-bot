from datetime import datetime, timedelta
from sqlalchemy import and_, or_, select
from database import session
from models import Leave, ManagerMap, Users
from util import calculate_leave_balance, mark_events, pad_text

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
    employee = session.query(Users).filter_by(slack_id=intern_filter).first()
    additional = [
        {
			"type": "context",
			"elements": [{
					"type": "mrkdwn",
					"text": f"Current Employee:"
				},
				{
					"type": "image",
					"image_url": employee.avatar,
					"alt_text": "cute cat"
				},
				{
					"type": "mrkdwn",
					"text": employee.name
				}
			]
		}]
    
    additional += [{
        "type": "context",
        "elements": [
            {
                "type": "mrkdwn",
                "text": calculate_leave_balance(intern_filter, employee.role == 'intern', False)
            }
        ]
    }]
        
    
    return additional