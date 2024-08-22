from database import Session
from models import ManagerMap
from generators import admin_home

def register(app):
    @app.action("duplicate_manager")
    def handle_duplicate(ack, client, body, logger):
        ack()
        session = Session()
        manager = body["actions"][0]["value"]
        users = session.query(ManagerMap.employee_id).filter_by(manager_id=manager).all()
        
        if len(users) > 0:
            client.views_open(
                trigger_id=body["trigger_id"],
                view={
                    "type": "modal",
                    "callback_id": "add_manager_submission",
                    "title": {"type": "plain_text", "text": "Duplicate Manager"},
                    "submit": {"type": "plain_text", "text": "Add"},
                    "blocks": [
                        {
                            "type": "section",
                            "text": {
                                "type": "plain_text",
                                "text": "Enter the details below to add a manager",
                                "emoji": True
                            }
                        },
                        {
                            "type": "input",
                            "element": {
                                "type": "users_select",
                                "placeholder": {
                                    "type": "plain_text",
                                    "text": "Select a manager",
                                    "emoji": True
                                },
                                "initial_user": manager,
                                "action_id": "manager_select"
                            },
                            "label": {
                                "type": "plain_text",
                                "text": "Select a Manager:",
                                "emoji": True
                            }
                        },{
                            "type": "input",
                            "element": {
                                "type": "multi_users_select",
                                "placeholder": {
                                    "type": "plain_text",
                                    "text": "Select employees",
                                    "emoji": True
                                },
                                "initial_users": [user[0] for user in users],
                                "action_id": "employee_select"
                            },
                            "label": {
                                "type": "plain_text",
                                "text": "Select Employees:",
                                "emoji": True
                            }
                        }
                    ]
                }
            )
        admin_home.generate(client, logger, user=body["user"]["id"])