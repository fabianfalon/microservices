from datetime import datetime

from sqlalchemy.dialects import mysql
from sqlalchemy.orm import relationship

from src.utils import DB

from .base_model import BaseModel
from .constants import ROLE_MAX_DESCRIPTION, ROLE_MAX_NAME


class Role(BaseModel):

    __tablename__ = "roles"

    name = DB.Column(DB.String(ROLE_MAX_NAME), name="name", nullable=False, comment="name")
    description = DB.Column(DB.String(ROLE_MAX_DESCRIPTION), name="description", nullable=False, comment="description")


class UserRole(BaseModel):
    __tablename__ = "user_role"
    id = DB.Column(
        DB.Integer,
        primary_key=True,
        autoincrement=True,
        comment="Internal identifier used as PK but not exposed outside this schema",
    )
    user_id = DB.Column(DB.Integer, DB.ForeignKey("user.id", name="user_id", ondelete="CASCADE"))
    role_id = DB.Column(DB.Integer, DB.ForeignKey(Role.id, ondelete="CASCADE"))
    creation_date = DB.Column(mysql.DATETIME(fsp=6), nullable=False, default=datetime.now)
    role = relationship("Role")
