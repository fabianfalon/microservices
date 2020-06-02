"""
Role serializer module
"""
from src.models.role import Role

from .common import CommonSchema


class RoleSchema(CommonSchema):
    class Meta:
        model = Role
        fields = ("id", "name")
