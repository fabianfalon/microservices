import logging

from flask import Blueprint
from flask_restful import Resource, Api
from ..services.got import got_service

got_blueprint = Blueprint('got', __name__)
api = Api(got_blueprint)
logger = logging.getLogger(__name__)


class GotPlaceResources(Resource):
    """Got resources"""

    def get(self):
        """Get all places """
        data = []
        # get to places services
        places = got_service.get_places()

        for place in places.get("results", []):
            # get peoples services
            people = got_service.get_people_by_place_id(place.get("id"))
            if people:
                data.append({
                    "id": place.get("id"),
                    "name": place.get("name"),
                    "people": people["results"]
                })
        return data, 200


class GotPlaceDetailResources(Resource):
    """Get place and peoples resources"""

    def get(self, place_id):
        """Get people by place"""
        # get to places services
        place = got_service.get_place_by_id(place_id)
        if place:
            # get to peoples services
            people = got_service.get_people_by_place_id(place.get("id"))
            data = {
                "id": place.get("id"),
                "name": place.get("name"),
                "people": people["results"]
            }
        return data, 200


api.add_resource(GotPlaceResources, '/v1/got/places/')
api.add_resource(GotPlaceDetailResources, '/v1/got/places/<place_id>')
