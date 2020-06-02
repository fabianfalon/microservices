""""
Service that manages creation and querying over Book,
"""
import logging

from src.models.user import User
from src.services.services import Service

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


usr_srv = UserService()
