import json

from tests.base import BaseTestCase
from tests.utils import add_people


class TestPeopleService(BaseTestCase):
    """Tests for the People Service."""

    def test_peoples(self):
        """Test people endpoint"""
        add_people("Persona 1", True, 2)
        add_people("Persona 2", True, 3)
        response = self.client.get('/v1/peoples/')
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["count"], 2)
        self.assertEqual(data["results"][0]["name"], "Persona 1")

    def test_peoples_not_fount(self):
        """Test people endpoint"""
        unknownId = 33
        response = self.client.get('/v1/peoples/{}'.format(unknownId))
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 404)
        self.assertEqual(
            data["message"], "People Not found with id: {}".format(unknownId)
        )

    def test_people_by_id(self):
        """Test people endpoint"""
        add_people("Persona 1", True, 2)
        people_id = 1
        response = self.client.get('/v1/peoples/{}'.format(people_id))
        self.assertEqual(response.status_code, 200)

    def test_get_people_by_place_id(self):
        """Test people endpoint"""
        add_people("Persona 1", True, 2)
        people_id = 1
        response = self.client.get(
            '/v1/peoples/place/{}'.format(people_id)
        )
        self.assertEqual(response.status_code, 200)
