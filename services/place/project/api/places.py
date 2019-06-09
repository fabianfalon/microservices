# services/places/project/api/places.py
# -*- coding: utf-8 -*-
import logging

from flask import Blueprint, jsonify
from flask_restful import Resource, Api, reqparse
from project import db
from sqlalchemy.orm import exc

from .models import Place

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
        places = [p.to_json() for p in Place.query.order_by(Place.id.asc())]
        response['results'] = places
        response['count'] = Place.query.count()
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
        try:
            place = Place.query.filter_by(id=place_id).one()
            response = place.to_json()
            return response, 200
        except (exc.NoResultFound, exc.MultipleResultsFound):
            logger.info("Place Not found with id: {}".format(place_id))
            response['message'] = "Place Not found with id: {}".format(place_id)
            response['error'] = True
            return response, 404

    def put(self, place_id):
        response = dict()
        data = self.parser.parse_args()
        if not data:
            response['message'] = "Place Bad request in update place {}, name field is mandatory".format(place_id)
            response['error'] = True
            return response, 400
        try:
            try:
                place = Place.query.filter_by(id=place_id).one()
                place.name = data["name"]
                db.session.commit()
                response['status'] = 'success'
                response['message'] = 'Place was updated!'
                response["data"] = place.to_json()
                return response, 200
            except exc.NoResultFound:
                logger.info("Place Bad request in update place {}".format(place_id))
                response['message'] = "Place: Bad request in update place {}, not found".format(place_id)
                response['error'] = True
                return response, 404
        except (exc.IntegrityError, ValueError, TypeError):
            db.session().rollback()
            logger.info("Place Bad request in update place {}".format(place_id))
            response['message'] = "Place: Bad request in update place {}".format(place_id)
            response['error'] = True
            return response, 400


api.add_resource(PlaceResources, '/v1/places/')
api.add_resource(PlaceDetailResources, '/v1/places/<place_id>')
