from generators import manager_home

def register(app):
    @app.action("summary_tab")
    def handle_summary_tab(ack, client, body, logger):
        ack()
        manager_home.generate(client, logger, user=body["user"]["id"], mode="summary")