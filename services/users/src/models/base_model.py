from datetime import datetime

from sqlalchemy import Column, Integer

from src.utils import DB


class BaseModel(DB.Model):
    __abstract__ = True

    id = Column(Integer, primary_key=True, autoincrement=True)

