import copy
import logging

from flask import Response, request
from flask_restplus import Resource, reqparse
from werkzeug.exceptions import BadRequest

from helpers import response_item, response_list, response_list_paginated
from src.models.constants import MAX_ELEMENT_PAGINATION_BOOK
from src.serializers.user import UserMinSchema
from src.services.user import usr_srv
from src.views.swagger_docs.api_model import API_USER
from src.views.swagger_docs.commons import MODEL_ERROR_LIST
from src.views.swagger_docs.user import MODEL_CREATE_USER, MODEL_DATA_USER_PAGINATED_LIST_PARENT, MODEL_UPDATE_USER
from src.views.validators.user import validate_user
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt()
TAG_WRAPPER = "user"
TAG_LIST_WRAPPER = "users"

logger = logging.getLogger("users")


@API_USER.route("users")
class User(Resource):
    @API_USER.doc(
        description="Get all users",
        responses={
            200: ("Recovers all status paginated", MODEL_DATA_USER_PAGINATED_LIST_PARENT),
            500: ("Internal Server Error", MODEL_ERROR_LIST),
        },
        params={
            "offset": {"description": "OFFSET", "type": "integer"},
            "limit": {"description": "LIMIT, default {}".format(MAX_ELEMENT_PAGINATION_BOOK), "type": "integer"},
            "authorId": {"description": "Author id", "type": "integer"},
        },
    )
    def get(self):

        parser = reqparse.RequestParser()
        parser.add_argument("offset", required=False, default=0, type=int, location="args")
        parser.add_argument("limit", required=False, default=MAX_ELEMENT_PAGINATION_BOOK, type=int, location="args")
        parser.add_argument("roleId", required=False, type=int, location="args")
        params = {}
        try:
            args = parser.parse_args()
        except BadRequest as err:
            raise Exception(message=err.data["message"], parameters=err.data["errors"])

        params.update({"offset": min(args.get("offset"), MAX_ELEMENT_PAGINATION_BOOK)})
        params.update({"limit": args.get("limit", 0)})
        params.update({"roleId": args.get("authorId", None)})

        params_dict = copy.deepcopy(params)
        params_dict.pop("offset", None)
        params_dict.pop("limit", None)

        users = usr_srv.get_paginated(offset=params.get("offset"), limit=params.get("limit"), params_dict=params_dict)
        return response_list_paginated(
            TAG_LIST_WRAPPER,
            users,
            serializer=UserMinSchema,
            base_link_pagination=request.base_url,
            query_params=params_dict,
        )


    @API_USER.expect(MODEL_CREATE_USER, description="Input data")
    @API_USER.doc(
        description="Create book",
        responses={
            201: ("Book created", MODEL_CREATE_USER),
            400: ("Input data wrong", MODEL_ERROR_LIST),
            403: ("User does not have enough permissions", MODEL_ERROR_LIST),
            406: ("Some of the requested languages are not available", MODEL_ERROR_LIST),
            409: ("Data conflict", MODEL_ERROR_LIST),
            500: ("Internal Server Error", MODEL_ERROR_LIST),
        },
    )
    def post(self):
        logger.debug("Creating Book")
        user_payload = request.get_json()
        validate_user(user_payload)
        user_payload["password"] = bcrypt.generate_password_hash(
            user_payload.get("password"), 13
        ).decode()
        user = usr_srv.create(user_payload)
        data = response_item(TAG_WRAPPER, user, serializer=UserMinSchema)
        return data, 201


@API_USER.route("users/<int:userId>")
class UserDetail(Resource):
    @API_USER.doc(
        description="Delete a user",
        responses={
            204: "User deleted",
            404: ("Book Entity not found", MODEL_ERROR_LIST),
            409: ("Data conflict", MODEL_ERROR_LIST),
            500: ("Internal Server Error", MODEL_ERROR_LIST),
        },
    )
    def delete(self, **kwargs):
        user_id = kwargs.get("userId")
        usr_srv.delete_by_id(user_id)
        return Response(status=204)

    @API_USER.doc(
        description="Detail user",
        responses={
            204: "Book detaild",
            404: ("User Entity not found", MODEL_ERROR_LIST),
            409: ("Data conflict", MODEL_ERROR_LIST),
            500: ("Internal Server Error", MODEL_ERROR_LIST),
        },
    )
    def get(self, **kwargs):
        user_id = kwargs.get("userId")
        user = usr_srv.get_by_id(user_id)
        return response_item(TAG_WRAPPER, user, serializer=UserMinSchema)
