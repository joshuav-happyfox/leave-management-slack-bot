from database import Session
from models import Users
from generators import admin_home

def register(app):
    @app.action("save_interns")
    def handle_save(ack, client, body, logger):
        session = Session()
        ack()

        interns = list(body['view']['state']['values'].values())[1]['intern_select']['selected_users']
        current_interns = session.query(Users).all()
        current_interns_ids = { intern.slack_id: intern for intern in current_interns }
        for intern in interns:
            if intern in current_interns_ids:
                current_interns_ids[intern].role = 'intern'
            else:
                session.add(Users(slack_id=intern, role='intern'))
       
        for intern in current_interns:
            if intern.slack_id not in interns:
                intern.role = 'employee'
        
        session.commit()
        admin_home.generate(client, logger, user=body["user"]["id"])