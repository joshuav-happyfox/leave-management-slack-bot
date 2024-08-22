from database import Session
from models import Leave, ManagerMap
from generators import employee_home, manager_home

def register(app):
    @app.action("approve_button")
    def handle_approve(ack, client, body, logger):
        session = Session()
        leave = session.query(Leave).get(body["actions"][0]["value"])
        
        if leave:
            leave.status = "accepted"
            session.add(leave)
            session.commit()
            ack()
            message = (
                f"Hi Intern!\n"
                f"You leave request for *{leave.start_date.strftime("%d %b %y")}* - *{leave.end_date.strftime("%d %b %y")}* has been `🟢 approved`"
            )
            client.chat_postMessage(
                channel=leave.user_id,
                text=message
            )
        managers = session.query(ManagerMap.manager_id).filter(ManagerMap.employee_id == leave.user_id).all()
        for manager_id in managers:
            manager_home.generate(client, logger, user=manager_id[0])
        employee_home.generate(client, logger, user=leave.user_id)