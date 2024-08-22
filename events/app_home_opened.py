from generators import employee_home, admin_home
from database import session
from models import Users

def register(app):
    @app.event("app_home_opened")
    def update_home_tab(client, event, logger):
        is_admin = session.query(Users).filter_by(slack_id=event["user"], is_admin=True).first()
        if is_admin:
            admin_home.generate(client, logger, user=event["user"])
        else:
            employee_home.generate(client, logger, user=event["user"])