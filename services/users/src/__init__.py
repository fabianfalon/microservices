import os
from flask import jsonify
from flask import Flask
from flask_cors import CORS
from flask_debugtoolbar import DebugToolbarExtension
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from src.exceptions import APIException

# instantiate the extensions
db = SQLAlchemy()
migrate = Migrate()
cors = CORS()
toolbar = DebugToolbarExtension()


def create_app(script_info=None):
    # instantiate the app
    app = Flask(__name__)

    # set config
    app_settings = os.getenv("APP_SETTINGS")
    app.config.from_object(app_settings)

    # set up extensions
    cors.init_app(app)
    toolbar.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)

    # register blueprints
    from src.views.people import peoples_blueprint

    app.register_blueprint(peoples_blueprint)

    # shell context for flask cli
    @app.shell_context_processor
    def ctx():
        return {"app": app, "db": db}

    @app.errorhandler(APIException)
    def generic_api_error_handler(error):
        response = jsonify(error.to_dict())
        response.status_code = error.status_code
        return response

    return app
