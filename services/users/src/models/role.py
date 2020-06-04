from sqlalchemy.orm import relationship

from src.models.user import User
from src.utils import DB

from .base_model import BaseModel
from .constants import ROLE_MAX_DESCRIPTION_LENGTH, ROLE_MAX_NAME_LENGTH


class Role(BaseModel):

    __tablename__ = "roles"

    name = DB.Column(DB.String(ROLE_MAX_NAME_LENGTH), name="name", nullable=False, comment="name")
    description = DB.Column(
        DB.String(ROLE_MAX_DESCRIPTION_LENGTH), name="description", nullable=False, comment="description"
    )

    @classmethod
    def create(cls, role):
        """
        Add role to database session

        :param role: role
        :return:
        """
        DB.session.add(role)
        DB.session.flush()


class UserRole(DB.Model):
    __tablename__ = "user_role"
    id = DB.Column(
        DB.Integer,
        primary_key=True,
        autoincrement=True,
        comment="Internal identifier used as PK but not exposed outside this schema",
    )
    user_id = DB.Column(DB.Integer, DB.ForeignKey(User.id, name="user_id", ondelete="CASCADE"))
    role_id = DB.Column(DB.Integer, DB.ForeignKey(Role.id, ondelete="CASCADE"))
    role = relationship("Role")
