from generators import manager_home

def register(app):
    @app.action("filter_dropdown")
    def handle_dropdown(ack, client, body, logger):
        ack()
        manager_home.generate(client, logger, user=body["user"]["id"], manager_filter=body["actions"][0]["selected_option"]['value'])