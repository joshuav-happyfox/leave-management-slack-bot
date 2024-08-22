from database import Session
from models import Users
from generators import admin_home

def register(app):
    @app.action("save_admins")
    def handle_save(ack, client, body, logger):
        session = Session()
        ack()
        
        admins = list(body['view']['state']['values'].values())[0]['admin_select']['selected_users']
        current = session.query(Users).all()
        current_ids = { admin.slack_id : admin for admin in current }
        for admin in admins:
            if admin in current_ids:
                current_ids[admin].is_admin = True
            else:
                session.add(Users(slack_id=admin, is_admin=True))
        
        for admin in current:
            if admin.slack_id not in admins and admin.slack_id != body["user"]["id"]:
                admin.is_admin = False

        session.commit()
        admin_home.generate(client, logger, user=body["user"]["id"])