from database import Session
from models import Leave, ManagerMap
from generators import employee_home, manager_home

def register(app):
    @app.action("delete_button")
    def handle_delete(ack, client, body, logger):
        session = Session()
        leave = session.query(Leave).get(body["actions"][0]["value"])
        
        if leave:
            session.delete(leave)
            session.commit()
            ack()
        employee_home.generate(client, logger, user=body["user"]["id"])
        managers = session.query(ManagerMap.manager_id).filter(ManagerMap.employee_id == body["user"]['id']).all()
        for manager_id in managers:
            manager_home.generate(client, logger, user=manager_id[0])