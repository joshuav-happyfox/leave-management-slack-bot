from generators import manager_menu
from util import main_header_generate, manager_header_generate


def generate(client, logger, user=None, manager_filter="view_all", intern_filter=None, mode="history"):
    additional = manager_menu.calendar_section.generate(user, manager_filter, intern_filter) if not intern_filter else manager_menu.employee_section.generate(user, manager_filter, intern_filter)
    additional_extra, show_dropdown = manager_menu.history_section.generate(user, manager_filter, intern_filter)
    additional += additional_extra
    try:
        client.views_publish(
            user_id=user,
            view={
                "type": "home",
                "callback_id": "home_view",
                "blocks": main_header_generate(user, "manager_tab", is_manager=True) + [
                {
                    "type": "section",
                    "text": {
                    "type": "mrkdwn",
                    "text": "*Hello Manager! Manage your _Intern Leaves_ here* :tada:"
                    }
                }] + show_dropdown + additional
            }
        )

    except Exception as e:
        logger.error(f"Error publishing home tab: {e}")