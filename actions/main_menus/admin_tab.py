from generators import admin_home

def register(app):
    @app.action("admin_tab")
    def handle_admin_tab(ack, client, body, logger):
        ack()
        admin_home.generate(client, logger, user=body["user"]["id"])