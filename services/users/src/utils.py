# -*- coding: utf-8 -*-
from functools import wraps
from cerberus import Validator
from cerberus.errors import BasicErrorHandler

from flask_babel import gettext
from werkzeug.exceptions import HTTPException
from flask_sqlalchemy import SQLAlchemy
from flask_sqlalchemy import BaseQuery as BaseQueryFlask
from enum import Enum


class BaseQuery(BaseQueryFlask):
    pass


DB = SQLAlchemy(query_class=BaseQuery)


class ErrorType(Enum):
    """
    Types of error included in http response body.
    """

    CRITICAL = "CRITICAL"
    FATAL = "FATAL"
    ERROR = "ERROR"
    WARNING = "WARNING"

    def serialize(self):
        """Return object in easily serializable format"""

        return self.value


class APIException(Exception):
    status_code = 400
    message = ""

    def __init__(self, message, status_code=None, payload=None, **kwargs):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload
        self.error_type = kwargs.get("error_type", ErrorType.ERROR)

    def to_dict(self):
        rv = dict(self.payload or ())
        rv["message"] = self.message
        rv["code"] = self.status_code
        rv["type"] = self.error_type.serialize()
        return rv


class IntegrityError(APIException):
    pass


class ResourceNotFound(APIException):
    status_code = 404
    message = "Not found"
    code = "ResourceNotFound"


class BadRequest(APIException):
    """
    Raise if the browser sends something to the application, the application
    or server cannot handle.
    """

    status_code = 400
    message = (
        "The request could not be completed due to something that is perceived as a client error "
        "(e.g., malformed request syntax, invalid request message framing, or deceptive request routing)."
    )
    code = "BadRequest"


def transactional(func):
    @wraps(func)
    def wrapped(*args, **kwargs):
        try:
            r = func(*args, **kwargs)
            DB.session.commit()
            return r
        except Exception as e:
            DB.session.rollback()
            raise e

    return wrapped



class CustomErrorHandler(BasicErrorHandler):
    def __init__(self, tree=None):
        super(CustomErrorHandler, self).__init__(tree)
        self.messages = BasicErrorHandler.messages.copy()
        messages_overwrite = {
            2: gettext("required field"),
            3: gettext("unknown field"),
            4: gettext("field '{0}' is required"),
            5: gettext("depends on these values: {constraint}"),
            34: gettext("empty values not allowed"),
            35: gettext("null value not allowed"),
            36: gettext("must be of {constraint} type"),
            39: gettext("min length is {constraint}"),
            40: gettext("max length is {constraint}"),
            65: gettext("value does not match regex '{constraint}'"),
            66: gettext("min value is {constraint}"),
            68: gettext("unallowed value {value}"),
        }
        self.messages.update(messages_overwrite)

    def __iter__(self):
        return super(CustomErrorHandler, self).__iter__()


def validate(schema, document, validator=Validator, update=False):
    """
    Validates document

    :param schema: Validator
    :param document: Document to be checked
    :param validator: Validator class to perform the validation
    :param update: If ``True``, required fields won't be checked.
    :return: Throw ApiException with custom format if error exists
    """
    if document is None:
        parameters = [dict(body="Impossible to validate input, mandatory body is missing")]
        raise BadRequest(message=gettext("BadRequestMessage"), parameters=parameters)
    validator = validator(schema, error_handler=CustomErrorHandler)
    if not validator.validate(document=document, update=update):
        parameters = [dict([(field, errors[0])]) for field, errors in validator.errors.items()]
        raise BadRequest(message=gettext("BadRequestMessage"), parameters=parameters)

    return True
