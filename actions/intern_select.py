from generators import manager_home

def register(app):
    @app.action("intern_select")
    def handle_intern_select(ack, client, body, logger):
        ack()
        manager_home.generate(client, logger, user=body["user"]["id"], intern_filter=body["actions"][0]["selected_user"], manager_filter="view_intern")