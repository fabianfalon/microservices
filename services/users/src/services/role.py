""""
Service that manages creation and querying over Book,
"""
import logging

from src.models.role import Role
from src.services.services import Service

logger = logging.getLogger("api")


class RoleService(Service):
    """
    Role Entity service.
    """

    entity = Role

    def get_paginated(self, offset: int, limit: int):
        entities = self.entity.query
        entities = entities.paginate(offset + 1, limit)
        return entities


role_srv = RoleService()
