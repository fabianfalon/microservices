"""
Author serializer module
"""

from src.models.user import User

from .common import CommonSchema


class UserMinSchema(CommonSchema):
    class Meta:
        model = User
        fields = ("id", "username", "email", "first_name", "last_name")
