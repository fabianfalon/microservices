import logging
from ..exceptions import ResourceNotFound
from ..models.place import Place

logger = logging.getLogger(__name__)


class PlaceService:
    """Place Service"""

    def get_by_id(self, id: int):
        place = Place.query.filter_by(id=id).first()
        if not place:
            logger.info("Place: Place Not found with id {id}".format(id=id))
            raise ResourceNotFound(
                message="Place Not found with id: {id}".format(id=id)
            )
        return place

    def get_all(self):
        places = [p.to_json() for p in Place.query.order_by(Place.id.asc())]
        return places

    def create(self, payload):
        place = Place()
        place.name = payload.get("name")
        place.save()
        logger.info("Place: place created successfuly")
        return place

    def update(self, id, payload):
        place = self.get_by_id(id)
        place = place.update(payload, commit=True)
        logger.info(
            "Place: place with id: {id} update successfuly".format(id=id)
        )
        return place


place_service = PlaceService()
