import logging

import requests
from flask import Blueprint, jsonify
from flask_restful import Resource, Api, reqparse
from ..exceptions import BadRequest
from ..services.people import people_service


peoples_blueprint = Blueprint('peoples', __name__)
api = Api(peoples_blueprint)
logger = logging.getLogger(__name__)


@peoples_blueprint.route('/peoples/ping', methods=['GET'])
def ping_pong():
    return jsonify({
        'status': 'success',
        'message': 'pong!'
    })


class PeopleResources(Resource):
    """People resources"""

    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument(
            'name', type=str, location='json', required=True
        )
        self.parser.add_argument(
            'isAlive', type=str, location='json', required=True
        )
        self.parser.add_argument(
            'placeId', type=str, location='json', required=True
        )
        self.parser.add_argument(
            'isKing', type=str, location='json', required=False
        )
        super(PeopleResources, self).__init__()

    def get(self):
        """Get all peoples"""
        response = dict()
        peoples = people_service.get_all()
        response['results'] = peoples
        response['count'] = len(peoples)
        return response, 200

    def post(self):
        """Create new people"""
        response = dict()
        data = self.parser.parse_args()
        place_response = requests.get(
            "http://places:5000/v1/places/{}".format(data.get("placeId"))
        )
        if place_response.ok:
            people = people_service.create(data)
            response['status'] = 'success'
            response['message'] = 'Person was created successfully'
            response['data'] = people.to_json()
            return response, 202
        else:
            error_message = place_response.json().get("message")
            raise BadRequest(message=error_message)


class PeopleDetailResources(Resource):
    """People detail Resources"""

    def get(self, people_id):
        """Get detail people"""
        response = dict()
        people = people_service.get_by_id(id=people_id)
        response = people.to_json()
        return response, 200


class PeopleByPlaceIdResources(Resource):
    """Get peoples by placeId"""

    def get(self, place_id):
        """Get detail people"""
        response = dict()
        try:
            peoples = people_service.get_people_by_place_id(place_id)
            response['results'] = peoples
            response['count'] = len(peoples)
            return response, 200
        except (exc.NoResultFound):
            logger.info("People Not found with place id: {}".format(place_id))
            response['message'] = "People Not found with place id: {}".format(place_id)
            response['error'] = True
            return response, 404


api.add_resource(PeopleResources, '/v1/peoples/')
api.add_resource(PeopleDetailResources, '/v1/peoples/<people_id>')
api.add_resource(PeopleByPlaceIdResources, '/v1/peoples/place/<place_id>')

