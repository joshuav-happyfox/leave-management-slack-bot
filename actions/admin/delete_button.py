from database import Session
from models import ManagerMap
from generators import admin_home

def register(app):
    @app.action("delete_manager")
    def handle_delete(ack, client, body, logger):
        session = Session()
        manager = session.query(ManagerMap).filter_by(manager_id=body["actions"][0]["value"]).all()
        
        if len(manager) > 0:
            for m in manager:
                session.delete(m)
            session.commit()
            ack()
        
        admin_home.generate(client, logger, user=body["user"]["id"])