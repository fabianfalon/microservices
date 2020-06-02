"""Module describing creation of flask applications.

.. moduleauthor:: Fabian Falon <fabian.falon@gmail.com>
.. versionadded:: 0.1.0
"""
import logging
import logging.config
from flask_babel import Babel

from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from pyms.flask.app import Microservice as MS

from src.views import BLUEPRINT as api
from swagger import swagger_bp
from src.utils import DB, APIException
from src.serializers.common import MA

logging.basicConfig()
logger = logging.getLogger("micro")
logger.setLevel(logging.DEBUG)
migration = Migrate()


class Microservice(MS):

    def init_libs(self):

        DB.init_app(self.application)
        babel = Babel(self.application)
        MA.init_app(self.application)
        if self.application.config["SWAGGER"]:
            self.application.register_blueprint(swagger_bp)

        self.application.register_blueprint(api)

        migration.init_app(self.application, DB)

        return self.application

    def init_logger(self):

        level = "DEBUG"

        LOGGING = {
            "version": 1,
            "disable_existing_loggers": True,
            "handlers": {
                "console": {"level": level, "class": "logging.StreamHandler",},
            },
            "loggers": {
                "": {"handlers": ["console"], "level": level, "propagate": True,},
                "anyconfig": {
                    "handlers": ["console"],
                    "level": "WARNING",
                    "propagate": True,
                },
                "pyms": {
                    "handlers": ["console"],
                    "level": "WARNING",
                    "propagate": True,
                },
                "root": {"handlers": ["console"], "level": level, "propagate": True,},
            },
        }

        logging.config.dictConfig(LOGGING)


def create_app():
    """Initialize the Flask app, register blueprints and intialize all libraries like Swagger, database, the trace system...
    return the app and the database objects.
    :return:
    """
    ms = Microservice(path=__file__)
    return ms.create_app()


app = create_app()


@app.errorhandler(APIException)
def generic_api_error_handler(exception):
    json_message = {"messages": [exception.to_dict()]}
    return json_message, exception.status_code


manager = Manager(app)

manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
    app.run(host='0.0.0.0', port=8000)
