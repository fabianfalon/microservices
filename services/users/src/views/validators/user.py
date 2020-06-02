from cerberus import Validator
from flask_babel import gettext
from src.utils import validate

from src.models.constants import USER_NAME_MAX_LENGTH, USER_FIRST_NAME_MAX_LENGTH, USER_LAST_NAME_MAX_LENGTH

SCHEMA_USER = {
    "username": {"type": "string", "empty": False, "maxlength": USER_NAME_MAX_LENGTH},
    "email": {"type": "string", "empty": False, "maxlength": 255},
    "first_name": {"type": "string", "empty": False, "maxlength": USER_FIRST_NAME_MAX_LENGTH},
    "last_name": {"type": "string", "empty": False, "maxlength": USER_LAST_NAME_MAX_LENGTH},
    "password": {"type": "string", "empty": False, "maxlength": 255},
}


class UserValidator(Validator):
    """
        Custom Validator to validate if name and description are different
    """

    def _validate_check_name_description(self, check_name_description, field, value):
        """
        The rule's arguments are validated against this schema: {'type': 'string'}

        :param check_name_description: flag for checking
        :param field: field key
        :param value: field value
        """
        if check_name_description and value == self.document.get("name"):
            self._error("description", gettext("name and description must be different"))


def validate_user(document, is_update=False):
    user_schema_validate = SCHEMA_USER.copy()
    return validate(user_schema_validate, document, validator=UserValidator, update=is_update)
