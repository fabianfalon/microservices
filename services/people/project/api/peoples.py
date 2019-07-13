# services/people/project/api/peoples.py
# -*- coding: utf-8 -*-
import logging

import requests
from flask import Blueprint, jsonify
from flask_restful import Resource, Api, reqparse
from project.api.models import People
from sqlalchemy.orm import exc

from .models import PeopleException

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
        peoples = [p.to_json() for p in People.query.order_by(People.id.asc())]
        response['results'] = peoples
        response['count'] = People.query.count()
        return response, 200

    def post(self):
        """Create new people"""
        response = dict()
        data = self.parser.parse_args()
        place_response = requests.get(
            "http://places:5000/v1/places/{}".format(data.get("placeId"))
        )
        if place_response.ok:
            isAlive = True if data.get("isAlive") == "True" else False
            isKing = True if data.get("isKing") == "True" else False
            people = People(
                name=data.get("name"),
                isAlive=isAlive, placeId=data.get("placeId"),
            )
            people.isKing = isKing
            try:
                people.save()
                response['status'] = 'success'
                response['message'] = 'Person was created successfully'
                response['data'] = people.to_json()
                return response, 202
            except PeopleException as error:
                logger.info(str(error))
                response['error'] = True
                response['message'] = str(error)
                return response, 400
        else:
            response['error'] = True
            response['message'] = 'Person could not be created because place was not found or doesnt exist'
            return response, 500


class PeopleDetailResources(Resource):
    """People detail Resources"""

    def get(self, people_id):
        """Get detail people"""
        response = dict()
        try:
            people = People.query.filter_by(id=people_id).one()
            response = people.to_json()
            return response, 200
        except (exc.NoResultFound, exc.MultipleResultsFound):
            logger.info("People Not found with id: {}".format(people_id))
            response['message'] = "People Not found with id: {}".format(people_id)
            response['error'] = True
            return response, 404


class PeopleByPlaceIdResources(Resource):
    """Get peoples by placeId"""

    def get(self, place_id):
        """Get detail people"""
        response = dict()
        try:
            peoples = [p.to_json() for p in People.query.filter_by(placeId=place_id).all()]
            response['results'] = peoples
            response['count'] = People.query.count()
            return response, 200
        except (exc.NoResultFound):
            logger.info("People Not found with place id: {}".format(place_id))
            response['message'] = "People Not found with place id: {}".format(place_id)
            response['error'] = True
            return response, 404


api.add_resource(PeopleResources, '/v1/peoples/')
api.add_resource(PeopleDetailResources, '/v1/peoples/<people_id>')
api.add_resource(PeopleByPlaceIdResources, '/v1/peoples/place/<place_id>')
