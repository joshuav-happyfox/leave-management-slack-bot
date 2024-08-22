from generators import manager_home

def register(app):
    @app.action("history_tab")
    def handle_history_tab(ack, client, body, logger):
        ack()
        manager_home.generate(client, logger, user=body["user"]["id"])