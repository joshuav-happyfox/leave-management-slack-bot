from database import Session
from models import ManagerMap
from generators import admin_home

def register(app):
    @app.action("edit_manager")
    def handle_edit(ack, client, body, logger):
        ack()
        session = Session()
        manager = body["actions"][0]["value"]
        users = session.query(ManagerMap.employee_id).filter_by(manager_id=manager).all()
        
        if len(users) > 0:
            client.views_open(
                trigger_id=body["trigger_id"],
                view={
                    "type": "modal",
                    "callback_id": "edit_manager_submission",
                    "title": {"type": "plain_text", "text": "Edit Manager"},
                    "submit": {"type": "plain_text", "text": "Edit"},
                    "blocks": [
                        {
                            "type": "section",
                            "text": {
                                "type": "plain_text",
                                "text": "Enter the details below to edit the manager",
                                "emoji": True
                            }
                        },
                        {
                            "type": "input",
                            "element": {
                                "type": "static_select",
                                "placeholder": {
                                    "type": "plain_text",
                                    "text": f"Select a Manager",
                                    "emoji": True
                                },
                                "options": [
                                    {
                                        "text": {
                                            "type": "plain_text",
                                            "text": f"<@{manager}>",
                                            "emoji": True
                                        },
                                        "value": manager
                                    },
                                ],
                                "initial_option": {
                                    "text": {
                                        "type": "plain_text",
                                        "text": f"<@{manager}>",
                                        "emoji": True
                                    },
                                    "value": manager
                                },
                                "action_id": "manager_select"
                            },
                            "label": {
                                "type": "plain_text",
                                "text": "Select Manager:",
                                "emoji": True
                            }
                        },
                        # {
                        #     "type": "section",
                        #     "text": {
                        #         "type": "mrkdwn",
                        #         "text": f"*Manager:* <@{manager}>"
                        #     }
                        # },
                        {
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