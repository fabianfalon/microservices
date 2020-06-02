from flask import Blueprint
from flask_restplus import Api
from pyms.flask.app import config

from src.utils import APIException
from src.views.swagger_docs.commons import API_DEFAULT as default_ns
from src.views.users import API_USER as users_ns

HTTP_500_INTERNAL_SERVER_ERROR = 500

# See /docs/archetype.rst -> Swagger section for more info about Swagger doc and spec
BLUEPRINT = Blueprint("api", __name__, url_prefix=config().URL_PREFIX)

API = Api(
    BLUEPRINT,
    title="Users Microservice",
    version=config().API_VERSION,
    description="Microservice to manage users",
    add_specs=True,
    authorizations={},
)

# Registers resources from namespace for current instance of api.
API.add_namespace(default_ns)
API.add_namespace(users_ns, path="/")


@API.errorhandler(APIException)
def generic_api_error_handler(exception):
    """
    """
    json_message = {"messages": [exception.to_dict()]}
    return json_message, exception.status_code


@API.errorhandler
def generic_error_handler(exception):
    """
    """
    api_exception = APIException(code=type(exception).__name__, message=str(exception), error_type="CRITICAL")
    json_message = {"messages": [api_exception.to_dict()]}
    return json_message, HTTP_500_INTERNAL_SERVER_ERROR
