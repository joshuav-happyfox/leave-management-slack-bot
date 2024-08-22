from database import session
from models import ManagerMap, Users
from util import main_header_generate, tab_menu

def generate(client, logger, user=None):
    additional = []
    managers_data = session.query(ManagerMap).all()
    admins = session.query(Users).filter_by(is_admin=True).all()
    interns = session.query(Users).filter_by(role='intern').all()
    managers = {}
    if len(managers_data) == 0:
        additional.append({
                "type": "section",
                "text": {
                    "type": "plain_text",
                    "emoji": True,
                    "text": "There are no managers at this moment."
                }
            })
    
    for manager_map in managers_data:
        manager_id = manager_map.manager_id
        if manager_id in managers:
            managers[manager_id].append(manager_map.employee_id)
        else:
            managers[manager_id] = [manager_map.employee_id]
    
    for manager_id in managers:
        additional += [{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": f"*Manager:* <@{manager_id}>\n\n Employees: " + ", ".join([f"<@{id}>" for id in managers[manager_id]])
			}
		},{
			"type": "actions",
			"elements": [
				{
					"type": "button",
					"text": {
						"type": "plain_text",
						"text": "Edit",
						"emoji": True
					},
					"value": str(manager_id),
					"action_id": "edit_manager"
				},{
					"type": "button",
					"text": {
						"type": "plain_text",
						"text": "Duplicate",
						"emoji": True
					},
					"value": str(manager_id),
					"action_id": "duplicate_manager"
				},{
					"type": "button",
					"text": {
						"type": "plain_text",
						"text": "Delete",
						"emoji": True
					},
                    "style": "danger",
					"value": str(manager_id),
					"action_id": "delete_manager"
				}
			]
		},{
            "type": "divider"
        }]
    
    try:
        client.views_publish(
        user_id=user,
        view={
            "type": "home",
            "callback_id": "home_view",

            "blocks": main_header_generate(user, "admin_tab", is_admin=True, is_manager=managers.get(user)) + [
            {
                "type": "section",
                "text": {
                "type": "mrkdwn",
                "text": "*Hello Admin! Manage your _Employees_ here* :tada:"
                }
            },
            {
                "type": "input",
                "element": {
                    "type": "multi_users_select",
                    "placeholder": {
                        "type": "plain_text",
                        "text": "Select admins",
                        "emoji": True
                    },
                    "initial_users": [admin.slack_id for admin in admins],
                    "action_id": "admin_select"
                },
                "label": {
                    "type": "plain_text",
                    "text": "Current Admins:",
                    "emoji": True
                }
            },
            {
                "type": "actions",
                "elements": [
                    {
                        "type": "button",
                        "text": {
                            "type": "plain_text",
                            "text": "Save",
                            "emoji": True
                        },
                        "action_id": "save_admins"
                    }
                ]
            },
            {
                "type": "divider"
            },
            {
                "type": "input",
                "element": {
                    "type": "multi_users_select",
                    "placeholder": {
                        "type": "plain_text",
                        "text": "Select interns",
                        "emoji": True
                    },
                    "initial_users": [user.slack_id for user in interns],
                    "action_id": "intern_select"
                },
                "label": {
                    "type": "plain_text",
                    "text": "Current Interns:",
                    "emoji": True
                }
            },
            {
                "type": "actions",
                "elements": [
                    {
                        "type": "button",
                        "text": {
                            "type": "plain_text",
                            "text": "Save",
                            "emoji": True
                        },
                        "action_id": "save_interns"
                    }
                ]
            },
            {
                "type": "divider"
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "Control the employees and managers they report to."
                },
                "accessory": {
                    "type": "button",
                    "style": "primary",
                    "text": {
                        "type": "plain_text",
                        "text": "Add a Manager"
                    },
                    "action_id": "add_manager_button",
                }
            },
            {
                "type": "section",
                "text": {
                "type": "mrkdwn",
                "text": "Current managers are:"
                }
            }
            ] + additional
        }
        )

    except Exception as e:
        logger.error(f"Error publishing home tab: {e}")