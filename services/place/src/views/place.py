import logging

from flask import Blueprint, jsonify
from flask_restful import Resource, Api, reqparse

from ..services.place import place_service
places_blueprint = Blueprint('places', __name__)
api = Api(places_blueprint)
logger = logging.getLogger(__name__)


@places_blueprint.route('/places/ping', methods=['GET'])
def ping_pong():
    return jsonify({
        'status': 'success',
        'message': 'pong!'
    })


class PlaceResources(Resource):
    """Place resources"""

    def get(self):
        """Get all places """
        response = dict()
        places = place_service.get_all()
        response['results'] = places
        response['count'] = len(places)
        return response, 200


class PlaceDetailResources(Resource):
    """Place Detail resources"""

    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument(
            'name', type=str, location='json', required=True
        )
        super(PlaceDetailResources, self).__init__()

    def get(self, place_id):
        """Get detail place"""
        response = dict()
        place = place_service.get_by_id(id=place_id)
        response = place.to_json()
        return response, 200

    def put(self, place_id):
        response = dict()
        data = self.parser.parse_args()
        if not data:
            err_msg = "Place: Bad request in update place {}, name field is mandatory".format(
                place_id
            )
            response['message'] = err_msg
            response['error'] = True
            return response, 400
        place = place_service.update(place_id, data)
        response['status'] = 'success'
        response['message'] = 'Place was updated!'
        response["data"] = place.to_json()
        return response, 200


api.add_resource(PlaceResources, '/v1/places/')
api.add_resource(PlaceDetailResources, '/v1/places/<place_id>')
