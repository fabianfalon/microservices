# services/place/project/tests/test_places.py
import json

from project.tests.base import BaseTestCase
from project.tests.utils import add_place


class TestPlaceService(BaseTestCase):
    """Tests for the Place Service."""

    def test_ping(self):
        """Ensure the /ping route behaves correctly."""
        response = self.client.get('/places/ping')
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertIn('pong!', data['message'])
        self.assertIn('success', data['status'])

    def test_places(self):
        """Test place endpoint"""
        add_place("Lugar 1")
        add_place("Lugar 2")
        response = self.client.get('/v1/places/')
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["count"], 2)
        self.assertEqual(data["results"][0]["name"], "Lugar 1")

    def test_places_not_fount(self):
        """Test place endpoint"""
        unknownId = 33
        response = self.client.get('/v1/places/{}'.format(unknownId))
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data["message"], "Place Not found with id: {}".format(unknownId))

    def test_places_by_id(self):
        """Test place endpoint"""
        add_place("Lugar 1")
        place_id = 1
        response = self.client.get('/v1/places/{}'.format(place_id))
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)

    def test_update_place(self):
        """Test place endpoint"""
        add_place("Lugar 1")
        place_id = 1
        updated_place_name = "Lugar 1 Edit"
        response = self.client.put(
            '/v1/places/{}'.format(place_id),
            data=json.dumps({'name': updated_place_name}),
            content_type='application/json'
        )
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["data"]["name"], updated_place_name)
