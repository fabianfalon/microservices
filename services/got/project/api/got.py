# services/got/project/api/peoples.py
# -*- coding: utf-8 -*-
import json
import logging

import requests
from flask import Blueprint
from flask_restful import Resource, Api

got_blueprint = Blueprint('got', __name__)
api = Api(got_blueprint)
logger = logging.getLogger(__name__)

PLACE_ENDPOINT = "http://places:5000/v1/places/"
PEOPLE_ENDPOINT = "http://peoples:5000/v1/peoples/"


class GotPlaceResources(Resource):
    """Got resources"""

    def get(self):
        """Get all places """
        data = []
        # get to places services
        places_response = requests.get(PLACE_ENDPOINT)
        if places_response.ok:
            place_data = json.loads(places_response.text)
            for place in place_data["results"]:
                # get to peoples services
                people_response = requests.get("{}place/{}".format(PEOPLE_ENDPOINT, place.get("id")))
                if people_response.ok:
                    people_data = json.loads(people_response.text)
                    data.append({
                        "id": place.get("id"),
                        "name": place.get("name"),
                        "people": people_data["results"]
                    })
        return data, 200


class GotPlaceDetailResources(Resource):
    """Get place and peoples resources"""

    def get(self, place_id):
        """Get people by place"""
        data = []
        peoples = []  # list of peoples
        # get to places services
        place_response = requests.get("{}{}".format(PLACE_ENDPOINT, place_id))
        if place_response.ok:
            # get to peoples services
            people_response = requests.get("{}place/{}".format(PEOPLE_ENDPOINT, place_id))
            if people_response.ok:
                people_data = json.loads(people_response.text)
                peoples = people_data["results"]
            place_data = json.loads(place_response.text)
            data.append({
                "id": place_data.get("id"),
                "name": place_data.get("name"),
                "people": peoples
            })
        return data, 200


api.add_resource(GotPlaceResources, '/v1/got/places/')
api.add_resource(GotPlaceDetailResources, '/v1/got/places/<place_id>')
