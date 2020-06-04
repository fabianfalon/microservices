"""Module describing creation of flask applications.

.. moduleauthor:: Fabian Falon <fabian.falon@gmail.com>
.. versionadded:: 0.1.0
"""
import logging
import logging.config
from flask_babel import Babel

from pyms.flask.app import Microservice as MS


logging.basicConfig()
logger = logging.getLogger("micro")
logger.setLevel(logging.DEBUG)


class Microservice(MS):

    def init_libs(self):
        babel = Babel(self.application)
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


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
