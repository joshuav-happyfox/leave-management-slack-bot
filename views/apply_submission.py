from datetime import datetime
from sqlalchemy import and_, or_
from models import Leave, ManagerMap
from util import get_month_ranges
from database import Session
from generators import employee_home, manager_home

def register(app):
    @app.view("apply_submission")
    def handle_submission(client, logger, ack, body):
        user = body['user']
        values = list(body['view']["state"]["values"].values())
        start_date = values[0]['from_date']['selected_date']
        end_date = values[1]['to_date']['selected_date']
        reason = values[2]['reason']['value']
        
        start_date_object = datetime.strptime(start_date, '%Y-%m-%d').date()
        end_date_object = datetime.strptime(end_date, '%Y-%m-%d').date()
        today_date = datetime.now().date()
        
        # Get the leave range split as a list for each month
        session = Session()
        existing_leave = session.query(Leave).filter(
            and_(
                Leave.user_id == user['id'], 
                Leave.status != "denied",
                or_(
                    and_(
                        Leave.start_date >= start_date,
                        Leave.start_date <= end_date
                    ),
                    and_(
                        Leave.end_date >= start_date,
                        Leave.end_date <= end_date
                    )
                )
        )).first()
        if existing_leave:
            errors = {
                'from_date': 'Selected date overlaps with existing leave.',
                'to_date': 'Selected date overlaps with existing leave.'
            }
            return ack({
                "response_action": 'errors',
                "errors": errors
            })
        elif end_date_object < start_date_object:
            errors = {
                'to_date': 'End date must be on or after start date.'
            }
            return ack({
                "response_action": 'errors',
                "errors": errors
            })
        elif start_date_object < today_date:
            print(start_date_object, today_date)
            errors = {
                'from_date': 'Start date must be on or after today.'
            }
            return ack({
                "response_action": 'errors',
                "errors": errors
            })
        ack()
        dates = get_month_ranges(start_date, end_date)
        
        for date in dates:
            application = Leave(
                user_name=user['username'],
                user_id=user['id'],
                start_date=date['start_date'],
                end_date=date['end_date'],
                duration=date['duration'],
                month=date['month'],
                year=date['year'],
                reason=reason
            )
            if date['duration'] == 0:
                errors = {
                    'from_date': 'Looks like its already a holiday (Weekends)',
                    'to_date': 'Looks like its already a holiday (Weekends)'
                }
                return ack({
                    "response_action": 'errors',
                    "errors": errors
                })
            session.add(application)
        
        session.commit()
        message = (
            f"Hi manager!\n"
            f"You have a new leave request from <@{user['id']}>"
        )
        employee_home.generate(client, logger, user=user["id"])
        managers = session.query(ManagerMap.manager_id).filter(ManagerMap.employee_id == user['id']).all()
        for manager_id in managers:
            client.chat_postMessage(
                channel=manager_id[0],
                text=message
            )
            manager_home.generate(client, logger, user=manager_id[0])
            
        