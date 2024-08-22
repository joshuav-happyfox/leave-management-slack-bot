from models import ManagerMap
from database import Session
from generators import admin_home

def register(app):
    @app.view("edit_manager_submission")
    def handle_edit_manager_submission(client, logger, ack, body):
        ack()
        values = list(body['view']["state"]["values"].values())
        manager = values[0]["manager_select"]["selected_option"]["value"]
        users = values[1]["employee_select"]["selected_users"]
        print(manager, users)
        
        session = Session()
        
        existing = session.query(ManagerMap).filter_by(manager_id=manager).all()
        
        existing_users = [user.employee_id for user in existing]
        
        for user_id in users:
            if user_id in existing_users or user_id == manager:
                continue
            manager_map = ManagerMap(manager_id=manager, employee_id=user_id)
            session.add(manager_map)
        
        for user_id in existing:
            if user_id.employee_id not in users:
                session.delete(user_id)
            
        session.commit()
        admin_home.generate(client, logger, user=body["user"]["id"])