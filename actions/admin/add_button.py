def register(app):
    @app.action("add_manager_button")
    def handle_add(ack, client, body, context):
        ack()
        client.views_open(
            trigger_id=body["trigger_id"],
            view={
                "type": "modal",
                "callback_id": "add_manager_submission",
                "title": {"type": "plain_text", "text": "Add Manager"},
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