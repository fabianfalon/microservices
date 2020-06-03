import time

import jwt
import requests
from flask import jsonify, request
from pyms.flask.app import config

from src.views import views_bp

KEY = "SECRET"


@views_bp.route("/login", methods=["POST"])
def login():
    """Healtcheck endpoint"""
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    base_url = config().CLIENTS.USERS.SERVER
    url = base_url + "/users/authenticate"
    response = requests.post(url, json={"username": username, "password": password})
    if response.ok:
        data = response.json()
        aud = "http://localhost:5000"
        now = int(time.time())
        token = {
            "iss": "http://localhost:8000",
            "aud": aud,
            "iat": now,
            "exp": now + 3600 * 24,
            "payload": data.get("data").get("user")
        }
        token = jwt.encode(token, KEY)
        return {"access_token": token.decode("utf8")}


@views_bp.route("/verify", methods=["POST"])
def verify_token():
    try:
        token = request.json["access_token"]
        audience = request.json.get("audience", "http://localhost:5000")
        return jwt.decode(token, KEY, audience=audience)
    except Exception as e:
        raise Exception("error")
