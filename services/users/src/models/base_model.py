import re
from sqlalchemy import Column, Integer

from src.utils import DB


class BaseModel(DB.Model):
    __abstract__ = True

    id = Column(Integer, primary_key=True, autoincrement=True)

    def mapping_fields(self, payload):
        for field in payload.keys():
            attribute_name = self.camel_case_to_snake_case(field)
            setattr(self, attribute_name, payload.get(field))
        return self

    def camel_case_to_snake_case(self, camel_str):
        s1 = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", camel_str)
        return re.sub("([a-z0-9])([A-Z])", r"\1_\2", s1).lower()

    def update(self, commit=True, **kwargs):
        for attr, value in kwargs.iteritems():
            setattr(self, attr, value)
        return commit and self.save() or self
