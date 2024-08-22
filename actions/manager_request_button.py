from database import Session
from models import Users
from util import main_header_generate

def register(app):
    @app.action("manager_request_button")
    def handle_request(ack, client, body, logger):
        session = Session()
        admins = [admin[0] for admin in session.query(Users.slack_id).filter_by(is_admin=True).all()]
        
        for admin in admins:
            message = (
                f"Hi Admin!\n"
                f"<@{body["user"]["id"]}> has requested for a manager to be assigned to them"
            )
            client.chat_postMessage(
                channel=admin,
                text=message
            )
            ack()
        try:
            client.views_publish(
                user_id=body["user"]["id"],
                view={
                    "type": "home",
                    "callback_id": "home_view",

                    "blocks": main_header_generate(body["user"]["id"]) + [
                    {
                        "type": "section",
                        "text": {
                        "type": "mrkdwn",
                        "text": "*Hello Intern! Manage your _Vacations_ here* :tada:"
                        }
                    },
                    {
                        "type": "divider"
                    },
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": "Your request has been sent successfully! Please wait before you request again."
                        },
                    },
                    ]
                }
                )

        except Exception as e:
            logger.error(f"Error publishing home tab: {e}")
        