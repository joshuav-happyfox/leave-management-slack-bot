from datetime import datetime
from database import session
from models import Leave
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

def generate(user=None, manager_filter="view_all", intern_filter=None):
    additional = [
    {
        "type": "section",
        "text": {
        "type": "mrkdwn",
        "text": "Manage & track all leave applications below:"
        }
    }
    ]
    leaves = session.query(Leave).all() if not intern_filter else session.query(Leave).filter_by(user_id=intern_filter).all()
    leaves.reverse()
    show_dropdown = []
    if manager_filter == 'view_intern':
        show_dropdown.append({
            "type": "users_select",
            "placeholder": {
                "type": "plain_text",
                "text": "All users",
                "emoji": True
            },
            "action_id": "intern_select"
        })
        
    if len(leaves) > 0:
        for leave in leaves:
            datestring = ""
            if leave.start_date.strftime("%d/%m/%Y") == leave.end_date.strftime("%d/%m/%Y"):
                datestring = leave.start_date.strftime("%d %b %y")
            else:
                datestring = f"{leave.start_date.strftime("%d %b %y")} - {leave.end_date.strftime("%d %b %y")}"
            additional.append({
                "type": "divider"
            })
            additional.append({
                "type": "section",
                "fields": [
                    {
                        "type": "mrkdwn",
                        "text": f"*Employee:*\n@{leave.user_name}"
                    },
                    {
                        "type": "mrkdwn",
                        "text": f"*Date:*\n{datestring}"
                    },
                    {
                        "type": "mrkdwn",
                        "text": f"*Status:*\n`{status[leave.status]} {leave.status}`"
                    },
                    {
                        "type": "mrkdwn",
                        "text": f"*Reason:*\n{leave.reason}"
                    },
                ]
            })
            if leave.status != 'pending':
                continue
            additional.append({
                "type": "actions",
                "elements": [
                    {
                        "type": "button",
                        "text": {
                            "type": "plain_text",
                            "emoji": True,
                            "text": "Approve"
                        },
                        "style": "primary",
                        "action_id": "approve_button",
                        "value": str(leave.id)
                    },
                    {
                        "type": "button",
                        "text": {
                            "type": "plain_text",
                            "emoji": True,
                            "text": "Deny"
                        },
                        "style": "danger",
                        "action_id": "deny_button",
                        "value": str(leave.id)
                    }
                ]
            })
    else:
        additional.append({
            "type": "section",
            "text": {
                "type": "plain_text",
                "emoji": True,
                "text": "_Looks like your interns are healthy & happy here. Good job!_"
            }
        })
    return additional, [{
                "type": "actions",
                "elements": [
                    {
                        "type": "static_select",
                        "placeholder": {
                            "type": "plain_text",
                            "text": "Select a filter",
                            "emoji": True
                        },
                        "options": [
                            {
                                "text": {
                                    "type": "plain_text",
                                    "text": "View all",
                                    "emoji": True
                                },
                                "value": "view_all"
                            },
                            {
                                "text": {
                                    "type": "plain_text",
                                    "text": "Filter by Intern",
                                    "emoji": True
                                },
                                "value": "view_intern"
                            }
                        ],
                        "initial_option": {
                            "text": {
                                "type": "plain_text",
                                "text": "View all",
                                "emoji": True
                            },
                            "value": "view_all"
                        } if manager_filter == 'view_all' else {
                                "text": {
                                    "type": "plain_text",
                                    "text": "Filter by Intern",
                                    "emoji": True
                                },
                                "value": "view_intern"
                            },
                        "action_id": "filter_dropdown"
                    },
                ] + show_dropdown,
            }]