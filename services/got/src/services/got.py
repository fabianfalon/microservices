import logging
import requests

from ..constants import PLACE_ENDPOINT, PEOPLE_ENDPOINT

logger = logging.getLogger(__name__)


class GotService:
    """GOT Service"""

    def get_places(self):
        response = requests.get(PLACE_ENDPOINT)
        if response.ok:
            return response.json()
        else:
            return []

    def get_place_by_id(self, place_id: int):
        response = requests.get("{}{}".format(PLACE_ENDPOINT, place_id))
        if response.ok:
            return response.json()
        else:
            return []

    def get_people_by_place_id(self, place_id: int):
        response = requests.get("{}place/{}".format(PEOPLE_ENDPOINT, place_id))
        if response.ok:
            return response.json()
        else:
            return []


got_service = GotService()
