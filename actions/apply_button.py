from datetime import datetime


def register(app):
    @app.action("apply_button")
    def handle_apply(ack, client, body, context):
        ack()
        today_date = datetime.now()
        client.views_open(
            # Pass a valid trigger_id within 3 seconds of receiving it
            trigger_id=body["trigger_id"],
            # View payload
            view={
                "type": "modal",
                # View identifier
                "callback_id": "apply_submission",
                "title": {"type": "plain_text", "text": "Leave Application"},
                "submit": {"type": "plain_text", "text": "Apply"},
                "blocks": [
                    {
                        "type": "section",
                        "text": {
                            "type": "plain_text",
                            "text": "Enter the details below to apply.",
                            "emoji": True
                        }
                    },
                    {
                        "type": "input",
                        "block_id": "from_date",
                        "element": {
                            "type": "datepicker",
                            "initial_date": today_date.strftime("%Y-%m-%d"),
                            "placeholder": {
                                "type": "plain_text",
                                "text": "Select a date",
                                "emoji": True
                            },
                            "action_id": "from_date"
                        },
                        "label": {
                            "type": "plain_text",
                            "text": "From",
                            "emoji": True
                        }
                    },
                    {
                        "type": "input",
                        "block_id": "to_date",
                        "element": {
                            "type": "datepicker",
                            "initial_date": today_date.strftime("%Y-%m-%d"),
                            "placeholder": {
                                "type": "plain_text",
                                "text": "Select a date",
                                "emoji": True
                            },
                            "action_id": "to_date"
                        },
                        "label": {
                            "type": "plain_text",
                            "text": "To",
                            "emoji": True
                        }
                    },
                    {
                        "type": "input",
                        "element": {
                            "type": "plain_text_input",
                            "action_id": "plain_text_input-action",
                            "multiline": True,
                            "action_id": "reason"
                        },
                        "label": {
                            "type": "plain_text",
                            "text": "Reason",
                            "emoji": True
                        }
                    }
                ]
            }
        )