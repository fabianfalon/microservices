""""
Service that manages creation and querying over Book,
"""
import logging
from src.models.user import User
from src.services.services import Service

from flask_bcrypt import Bcrypt
bcrypt = Bcrypt()

logger = logging.getLogger("api")


class UserService(Service):
    """
    Book Entity service.
    """

    entity = User

    def get_paginated(self, offset: int, limit: int, params_dict={}):
        entities = self.entity.query
        entities = entities.paginate(offset + 1, limit)
        return entities

    def get_by_username(self, username):
        entity = self.entity.query.filter_by(username=username).first()
        return entity

    def authenticated(self, username, password):
        user = self.entity.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(
            user.password, password
        ):
            return user


usr_srv = UserService()
