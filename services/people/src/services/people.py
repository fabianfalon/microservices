import logging
from ..exceptions import ResourceNotFound
from ..models.people import People

logger = logging.getLogger(__name__)


class PeopleService:
    """People Service"""

    def get_by_id(self, id: int):
        people = People.query.filter_by(id=id).first()
        if not people:
            logger.info("People: People Not found with id {id}".format(id=id))
            raise ResourceNotFound(
                message="People Not found with id: {id}".format(id=id)
            )
        return people

    def get_all(self):
        peoples = [p.to_json() for p in People.query.order_by(People.id.asc())]
        return peoples

    def get_people_by_place_id(self, place_id):
        peoples = [p.to_json() for p in People.query.filter_by(placeId=place_id).all()]
        return peoples

    def create(self, payload):
        isAlive = True if payload.get("isAlive") == "True" else False
        isKing = True if payload.get("isKing") == "True" else False
        people = People(
            name=payload.get("name"),
            isAlive=isAlive, placeId=payload.get("placeId"),
        )
        people.isKing = isKing
        people.save()
        logger.info(
            "People: people created successfuly".format(id=id)
        )
        return people

    def update(self, id, payload):
        people = self.get_by_id(id)
        people = people.update(payload, commit=True)
        logger.info(
            "People: people with id: {id} update successfuly".format(id=id)
        )
        return people


people_service = PeopleService()
