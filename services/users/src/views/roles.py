import copy
import logging

from flask import Response, request
from flask_restplus import Resource, reqparse
from werkzeug.exceptions import BadRequest

from helpers import response_item, response_list, response_list_paginated
from src.models.constants import MAX_ELEMENT_PAGINATION
from src.serializers.role import RoleSchema
from src.services.role import role_srv
from src.views.swagger_docs.api_model import API_ROLE
from src.views.swagger_docs.commons import MODEL_ERROR_LIST
from src.views.swagger_docs.role import MODEL_CREATE_ROLE, MODEL_DATA_ROLE_PAGINATED_LIST_PARENT

TAG_WRAPPER = "role"
TAG_LIST_WRAPPER = "roles"

logger = logging.getLogger("roles")


@API_ROLE.route("roles")
class Role(Resource):
    @API_ROLE.doc(
        description="Get all roles",
        responses={
            200: ("Recovers all status paginated", MODEL_DATA_ROLE_PAGINATED_LIST_PARENT),
            500: ("Internal Server Error", MODEL_ERROR_LIST),
        },
        params={
            "offset": {"description": "OFFSET", "type": "integer"},
            "limit": {"description": "LIMIT, default {}".format(MAX_ELEMENT_PAGINATION), "type": "integer"},
        },
    )
    def get(self):

        parser = reqparse.RequestParser()
        parser.add_argument("offset", required=False, default=0, type=int, location="args")
        parser.add_argument("limit", required=False, default=MAX_ELEMENT_PAGINATION, type=int, location="args")
        params = {}
        try:
            args = parser.parse_args()
        except BadRequest as err:
            raise Exception(message=err.data["message"], parameters=err.data["errors"])

        params.update({"offset": min(args.get("offset"), MAX_ELEMENT_PAGINATION)})
        params.update({"limit": args.get("limit", 0)})

        params_dict = copy.deepcopy(params)
        params_dict.pop("offset", None)
        params_dict.pop("limit", None)

        roles = role_srv.get_paginated(offset=params.get("offset"), limit=params.get("limit"), params_dict=params_dict)
        return response_list_paginated(
            TAG_LIST_WRAPPER,
            roles,
            serializer=RoleSchema,
            base_link_pagination=request.base_url,
            query_params=params_dict,
        )

    @API_ROLE.expect(MODEL_CREATE_ROLE, description="Input data")
    @API_ROLE.doc(
        description="Create role",
        responses={
            201: ("Role created", MODEL_CREATE_ROLE),
            400: ("Input data wrong", MODEL_ERROR_LIST),
            403: ("User does not have enough permissions", MODEL_ERROR_LIST),
            406: ("Some of the requested languages are not available", MODEL_ERROR_LIST),
            409: ("Data conflict", MODEL_ERROR_LIST),
            500: ("Internal Server Error", MODEL_ERROR_LIST),
        },
    )
    def post(self):
        logger.debug("Creating new Role")
        payload = request.get_json()
        role = role_srv.create(payload)
        data = response_item(TAG_WRAPPER, role, serializer=RoleSchema)
        return data, 201
