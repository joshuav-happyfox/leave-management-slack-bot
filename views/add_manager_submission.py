from models import ManagerMap
from database import Session
from generators import admin_home

def register(app):
    @app.view("add_manager_submission")
    def handle_add_manager_submission(client, logger, ack, body):
        ack()
        values = list(body['view']["state"]["values"].values())
        manager = values[0]["manager_select"]["selected_user"]
        users = values[1]["employee_select"]["selected_users"]
        print(manager, users)
        
        session = Session()
        
        existing_users = session.query(ManagerMap.employee_id).filter_by(employee_id=manager).all()
        
        for user_id in users:
            if user_id in existing_users or user_id == manager:
                continue
            manager_map = ManagerMap(manager_id=manager, employee_id=user_id)
            session.add(manager_map)
        
        session.commit()
        admin_home.generate(client, logger, user=body["user"]["id"])