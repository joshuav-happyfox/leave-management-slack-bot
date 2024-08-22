import os
from dotenv import load_dotenv

from util import init_admin 
load_dotenv() 

from slack_bolt import App
import events
import actions
import views


app = App(
    token=os.getenv("TOKEN"),
    signing_secret=os.getenv("SIGNING_SECRET")
)

def register_events(app):
    events.app_home_opened.register(app)

def register_actions(app):
    actions.apply_button.register(app)
    actions.delete_button.register(app)
    actions.deny_button.register(app)
    actions.approve_button.register(app)
    actions.intern_select.register(app)
    actions.filter_dropdown.register(app)
    actions.manager_request_button.register(app)
    
    actions.admin.add_button.register(app)
    actions.admin.delete_button.register(app)
    actions.admin.duplicate_button.register(app)
    actions.admin.edit_button.register(app)
    actions.admin.save_admins.register(app)
    actions.admin.save_interns.register(app)
    
    actions.main_menus.employee_tab.register(app)
    actions.main_menus.manager_tab.register(app)
    actions.main_menus.admin_tab.register(app)
    
    actions.manager_menu.history_tab.register(app)
    actions.manager_menu.summary_tab.register(app)    
    
def register_views(app):
    views.apply_submission.register(app)
    views.add_manager_submission.register(app)
    views.edit_manager_submission.register(app)


if __name__ == "__main__":
    register_events(app)
    register_actions(app)
    register_views(app)
    init_admin()
    app.start(port=int(os.getenv("PORT", 3000)))