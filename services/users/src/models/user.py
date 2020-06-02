import re

from src.utils import DB

from .base_model import BaseModel
from .constants import USER_FIRST_NAME_MAX_LENGTH, USER_LAST_NAME_MAX_LENGTH, USER_NAME_MAX_LENGTH


class User(BaseModel):

    __tablename__ = "users"

    username = DB.Column(DB.String(USER_NAME_MAX_LENGTH), name="username", nullable=False, comment="username")
    email = DB.Column(DB.String(255), name="email", nullable=False, comment="email")
    first_name = DB.Column(
        DB.String(USER_FIRST_NAME_MAX_LENGTH), name="first_name", nullable=False, comment="first_name"
    )
    last_name = DB.Column(DB.String(USER_LAST_NAME_MAX_LENGTH), name="last_name", nullable=False, comment="last_name")
    password = DB.Column(DB.String(255), name="password", nullable=False, comment="password")

    @classmethod
    def create(cls, user):
        """
        Add user to database session

        :param user: user
        :return:
        """
        DB.session.add(user)
        DB.session.flush()

    def update(self, commit=True, **kwargs):
        for attr, value in kwargs.iteritems():
            setattr(self, attr, value)
        return commit and self.save() or self

    def mapping_fields(self, payload):
        """
        Maps from dictionary to target object. Special cases are considered to avoid data overwriting: when object is
        being created for the first time or some data is missing in source payload

        :param payload: dictionary with new data
        :return: target object filled with payload data
        """
        for field in payload.keys():
            attribute_name = self.camel_case_to_snake_case(field)
            setattr(self, attribute_name, payload.get(field))
        return self

    def camel_case_to_snake_case(self, camel_str):
        s1 = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", camel_str)
        return re.sub("([a-z0-9])([A-Z])", r"\1_\2", s1).lower()
