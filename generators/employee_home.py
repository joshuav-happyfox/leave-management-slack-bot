from datetime import datetime
from database import session
from models import Leave, ManagerMap, Users
from util import calculate_leave_balance, main_header_generate

status = {
    'pending': "🟡",
    'accepted': "🟢",
    'denied': "🔴"
}

def displayDelete(leave):
    if leave.status == 'denied':
        return False
    elif leave.status == 'accepted' and leave.start_date <= datetime.now().date():
        return False
    return True


def generate(client, logger, user=None, manager_filter="view_all", intern_filter=None):
    additional = []
    leaves = session.query(Leave).filter_by(user_id=user).all()
    leaves.reverse()
    is_intern = bool(session.query(Users).filter_by(role='intern').first())
    
    managers = [m[0] for m in session.query(ManagerMap.manager_id).filter_by(employee_id=user).all()]
    
    if len(managers) == 0:
        try:
            client.views_publish(
                user_id=user,
                view={
                    "type": "home",
                    "callback_id": "home_view",

                    "blocks": main_header_generate(user) + [
                    {
                        "type": "section",
                        "text": {
                        "type": "mrkdwn",
                        "text": f"*Hello {'Intern' if is_intern else 'Employee'}! Manage your _Vacations_ here* :tada:"
                        }
                    },
                    {
                        "type": "divider"
                    },
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": "Looks like you're not assigned a manager to apply for leaves. Request the administrator to assign a manager for you."
                        },
                        "accessory": {
                            "type": "button",
                            "style": "primary",
                            "text": {
                                "type": "plain_text",
                                "text": "Request a Manager"
                            },
                            "action_id": "manager_request_button",
                        }
                    },
                    ]
                }
                )

        except Exception as e:
            logger.error(f"Error publishing home tab: {e}")
        return
        
    
    # Calculate leave balance
    leaveText = calculate_leave_balance(user, is_intern)
    
    if len(leaves) > 0:
        for leave in leaves:
            datestring = ""
            if leave.start_date.strftime("%d/%m/%Y") == leave.end_date.strftime("%d/%m/%Y"):
                datestring = leave.start_date.strftime("%d %b %y")
            else:
                datestring = f"{leave.start_date.strftime("%d %b %y")} - {leave.end_date.strftime("%d %b %y")}"
            additional.append({
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"🗓️ *{datestring}* _({leave.duration} days)_\n*Status*: `{status[leave.status]} {leave.status}`\n*Reason*: {leave.reason}"
                },
                "accessory": {
                    "type": "button",
                    "style": "danger",
                    "text": {
                        "type": "plain_text",
                        "emoji": True,
                        "text": "Delete"
                    },
                    "action_id": "delete_button",
                    "value": str(leave.id)
                } 
            } if displayDelete(leave) else {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"🗓️ *{datestring}* _({leave.duration} days)_\n*Status*: `{status[leave.status]} {leave.status}`\n*Reason*: {leave.reason}"
                }
            })
    else:
        additional.append({
            "type": "section",
            "text": {
                "type": "plain_text",
                "emoji": True,
                "text": "_Looks like your slate is clean. Good job!_"
            }
        })
    # Render the view for the person
    try:
        client.views_publish(
        user_id=user,
        view={
            "type": "home",
            "callback_id": "home_view",

            "blocks": main_header_generate(user) + [
            {
                "type": "section",
                "text": {
                "type": "mrkdwn",
                "text": f"*Hello {'Intern' if is_intern else 'Employee'}! Manage your _Vacations_ here* :tada:"
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "Your leave applications can be applied, tracked and managed here without hassle."
                },
                "accessory": {
                    "type": "button",
                    "style": "primary",
                    "text": {
                        "type": "plain_text",
                        "text": "Apply for a leave"
                    },
                    "action_id": "apply_button",
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": leaveText
                },
            },
            {
                "type": "divider"
            },
            {
                "type": "section",
                "text": {
                "type": "mrkdwn",
                "text": "Manage & track your leave applications below:"
                }
            }
            ] + additional
        }
        )

    except Exception as e:
        logger.error(f"Error publishing home tab: {e}")