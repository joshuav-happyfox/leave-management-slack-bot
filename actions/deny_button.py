from database import Session
from models import Leave, ManagerMap
from generators import employee_home, manager_home

def register(app):
    @app.action("deny_button")
    def handle_deny(ack, client, body, logger):
        session = Session()
        leave = session.query(Leave).get(body["actions"][0]["value"])
        
        if leave:
            leave.status = "denied"
            session.add(leave)
            session.commit()
            ack()
            message = (
                f"Hi Intern!\n"
                f"You leave request for *{leave.start_date.strftime("%d %b %y")}* - *{leave.end_date.strftime("%d %b %y")}* has been `🔴 denied`"
            )
            client.chat_postMessage(
                channel=leave.user_id,
                text=message
            )
        
        managers = session.query(ManagerMap.manager_id).filter(ManagerMap.employee_id == leave.user_id).all()
        for manager_id in managers:
            manager_home.generate(client, logger, user=manager_id[0])
        
        # manager_home.generate(client, logger, user=body["user"]["id"])
        employee_home.generate(client, logger, user=leave.user_id)