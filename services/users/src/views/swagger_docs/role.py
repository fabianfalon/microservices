"""    sa.Column('creation_date', mysql.DATETIME(fsp=6), nullable=False),
API Model docs module    sa.Column('creation_date', mysql.DATETIME(fsp=6), nullable=False),
"""
from flask_restplus import Namespace, fields
from src.models.constants import ROLE_MAX_NAME_LENGTH, ROLE_MAX_DESCRIPTION_LENGTH

from .commons import MODEL_PAGINATION

API_ROLE = Namespace("Roles", description="roles")
MODEL_ROLE_DATA = API_ROLE.model("Role", {"id": fields.String(description="Unique identifier")})

MODEL_ROLE = API_ROLE.model("Role", {"id": fields.Integer, "name": fields.String, "description": fields.String})

MODEL_DATA_ROLE_PAGINATED_LIST_PARENT = API_ROLE.model(
    "RolePaginatedListParent",
    {"role": fields.List(fields.Nested(MODEL_ROLE)), "pagination": fields.Nested(MODEL_PAGINATION)},
)

MODEL_CREATE_ROLE = API_ROLE.model(
    "CreateRole",
    {
        "name": fields.String(description="User username", max_length=ROLE_MAX_NAME_LENGTH),
        "description": fields.String(description="User email", max_length=ROLE_MAX_DESCRIPTION_LENGTH),
    },
)


MODEL_UPDATE_ROLE = API_ROLE.model(
    "UpdateRole",
    {
        "name": fields.String(description="User username", max_length=ROLE_MAX_NAME_LENGTH),
        "description": fields.String(description="User email", max_length=ROLE_MAX_DESCRIPTION_LENGTH),
    },
)
