""""
Service
"""
import logging
from src.exceptions import ResourceNotFound
from src.utils import transactional

logger = logging.getLogger("api")


class Service:
    entity = None

    @transactional
    def create(self, payload):
        instance = self.entity()
        row = instance.mapping_fields(payload)
        self.entity.create(row)
        return row

    @transactional
    def update(self, entity_id, payload):
        instance = self.get_by_id(entity_id)
        return instance.mapping_fields(payload)

    def get_by_id(self, entity_id: int):
        entity = self.entity.query.filter_by(id=entity_id).first()
        if entity:
            return entity
        else:
            raise ResourceNotFound(message="Entity with id: {id}".format(id=entity_id))
