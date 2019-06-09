# services/people/project/__init__.py
import os

from flask import Flask
from flask_cors import CORS
from flask_debugtoolbar import DebugToolbarExtension
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

# instantiate the extensions
db = SQLAlchemy()
migrate = Migrate()
cors = CORS()
toolbar = DebugToolbarExtension()


def create_app(script_info=None):
    # instantiate the app
    app = Flask(__name__)

    # set config
    app_settings = os.getenv('APP_SETTINGS')
    app.config.from_object(app_settings)

    # set up extensions
    cors.init_app(app)
    toolbar.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)

    # register blueprints
    from project.api.peoples import peoples_blueprint
    app.register_blueprint(peoples_blueprint)

    # shell context for flask cli
    @app.shell_context_processor
    def ctx():
        return {
            'app': app,
            'db': db
        }

    return app
