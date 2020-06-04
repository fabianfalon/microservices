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
