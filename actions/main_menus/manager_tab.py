from generators import manager_home

def register(app):
    @app.action("manager_tab")
    def handle_manager_tab(ack, client, body, logger):
        ack()
        manager_home.generate(client, logger, user=body["user"]["id"])