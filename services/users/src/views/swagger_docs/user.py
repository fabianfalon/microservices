"""
API Model docs module
"""
from flask_restplus import Namespace, fields
from src.models.constants import USER_NAME_MAX_LENGTH, USER_FIRST_NAME_MAX_LENGTH, USER_LAST_NAME_MAX_LENGTH

from .commons import MODEL_PAGINATION

API_USER = Namespace("Users", description="users")
MODEL_USER_DATA = API_USER.model("User", {"id": fields.String(description="Unique identifier")})

MODEL_USER = API_USER.model(
    "User",
    {
        "id": fields.Integer,
        "username": fields.String,
        "email": fields.String,
        "first_name": fields.String,
        "last_name": fields.String,
        "creationDate": fields.DateTime(
            description="Creation date time. String in ISO 8601 format, " "YYYY-MM-DDTHH:MM:SS[.mmmmmm][+HH:MM]"
        ),
        "modificationDate": fields.DateTime(
            description="Creation date time. String in ISO 8601 format, " "YYYY-MM-DDTHH:MM:SS[.mmmmmm][+HH:MM]"
        ),
    },
)

MODEL_DATA_USER_PAGINATED_LIST_PARENT = API_USER.model(
    "UserPaginatedListParent",
    {"user": fields.List(fields.Nested(MODEL_USER)), "pagination": fields.Nested(MODEL_PAGINATION)},
)


MODEL_CREATE_USER = API_USER.model(
    "CreateUser",
    {
        "username": fields.String(description="User username", max_length=USER_NAME_MAX_LENGTH),
        "email": fields.String(description="User email", max_length=500),
        "first_name": fields.String(description="User first_name", max_length=USER_FIRST_NAME_MAX_LENGTH),
        "last_name": fields.String(description="User last_name", max_length=USER_LAST_NAME_MAX_LENGTH),
    },
)


MODEL_USER_AUTHENTICATED = API_USER.model(
    "UserAuthenthicated",
    {
        "username": fields.String(description="User username", max_length=USER_NAME_MAX_LENGTH),
        "password": fields.String(description="User email", max_length=500),
    },
)


MODEL_UPDATE_USER = API_USER.model(
    "UpdateUser",
    {
        "first_name": fields.String(description="User first_name", max_length=USER_FIRST_NAME_MAX_LENGTH),
        "last_name": fields.String(description="User last_name", max_length=USER_LAST_NAME_MAX_LENGTH),
    },
)
