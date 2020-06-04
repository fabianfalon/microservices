"""        "name": fields.String(description="User username", max_length=ROLE_NAME_MAX_LENGTH),
        "description": fields.String(description="User email", max_length=ROLE_MAX_DESCRIPTION_LENGTH
API Model docs module
"""
from src.views.swagger_docs.user import API_USER, MODEL_USER_DATA
from src.views.swagger_docs.role import API_ROLE, MODEL_ROLE_DATA
