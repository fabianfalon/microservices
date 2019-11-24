import os

from flask import Flask
from flask_cors import CORS

cors = CORS()


def create_app(script_info=None):
    # instantiate the app
    app = Flask(__name__)

    # set config
    app_settings = os.getenv('APP_SETTINGS')
    app.config.from_object(app_settings)

    # set up extensions
    cors.init_app(app)

    # register blueprints
    from project.api.got import got_blueprint
    app.register_blueprint(got_blueprint)

    # shell context for flask cli
    @app.shell_context_processor
    def ctx():
        return {'app': app}

    return app
