from generators import employee_home

def register(app):
    @app.action("employee_tab")
    def handle_employee_tab(ack, client, body, logger):
        ack()
        employee_home.generate(client, logger, user=body["user"]["id"])