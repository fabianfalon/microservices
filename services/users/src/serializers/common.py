import re
from copy import deepcopy
from urllib.parse import urlencode

from flask_marshmallow import Marshmallow
from marshmallow import fields, post_dump


def snake_case_to_camel_case(snake_str):
    components = snake_str.split("_")
    return components[0] + "".join(x.title() for x in components[1:])


def add_is_prefix(text):
    if len(text) > 1:
        capitalized = "%s%s" % (text[0].upper(), text[1:])
    else:
        capitalized = text.capitalize()
    return "is" + capitalized


def dictionary_format_convention(dictionary):
    data_copy = deepcopy(dictionary)
    for key, value in dictionary.items():
        convention_key = snake_case_to_camel_case(key)
        if isinstance(value, bool):
            convention_key = add_is_prefix(convention_key)
        data_copy[convention_key] = value
        if convention_key != key:
            del data_copy[key]
    return data_copy


MA = Marshmallow()


class CommonSchema(MA.Schema):
    creation_date = fields.Method("get_creation_date")
    modification_date = fields.Method("get_modification_date")

    @staticmethod
    def get_creation_date(obj):
        return obj.creation_date.isoformat()

    @staticmethod
    def get_modification_date(obj):
        return obj.modification_date.isoformat()

    @staticmethod
    def data_to_cammel_case(data):
        data_copy = deepcopy(data)
        for (key, value) in data.items():
            key_camel = snake_case_to_camel_case(key)
            data_copy[key_camel] = value
            if key_camel != key:
                del data_copy[key]
        return data_copy

    @post_dump
    def wrapper_data(self, data):
        return dictionary_format_convention(data)


class PaginationSchema(CommonSchema):

    next = fields.Method("get_next_links")
    previous = fields.Method("get_prev_links")

    class Meta:
        fields = ("pages", "per_page", "total", "previous", "next", "page")

    def get_total_pages(self, obj):
        return obj.pages

    def get_prev_links(self, obj):
        base_link_pagination = self.context["base_link_pagination"]
        params = self.get_query_params(obj)
        if obj.prev_num:
            offset = obj.prev_num - 1
            kwargs = {"limit": obj.per_page, "offset": offset}
            return self.make_url(base_link_pagination, params, kwargs)
        else:
            return None

    @staticmethod
    def make_url(base_link, params, pagination):
        if params:
            return base_link + "?" + urlencode(pagination) + params
        else:
            return base_link + "?" + urlencode(pagination)

    def get_next_links(self, obj):
        base_link_pagination = self.context["base_link_pagination"]
        params = self.get_query_params(obj)
        if obj.next_num:
            offset = obj.next_num - 1
            kwargs = {"limit": obj.per_page, "offset": offset}
            return self.make_url(base_link_pagination, params, kwargs)
        else:
            return None

    def get_query_params(self, obj):
        """
        Constructs a String with all the valid params except for those in excluded list

        :param excluded: list of excluded params
        """
        if not self.context["query_params"]:
            return ""

        params = {}
        for key, value in list(self.context["query_params"].items()):
            if value:
                params[key] = value
        # If there aren't query params to add after matching exclusions
        if not params:
            return ""
        return "&" + urlencode(params)

    @post_dump
    def rename_field(self, data):
        """

        :param data: Data dumped in serialization
        :return: Data with rename names based on BBVA's standards
        """
        rename_fields = {
            "page": data["page"],
            "totalPages": data["pages"],
            "totalElements": data["total"],
            "pageSize": data["per_page"],
        }
        data.update(rename_fields)
        for key_to_delete in "pages", "total", "per_page":
            del data[key_to_delete]

        return data
