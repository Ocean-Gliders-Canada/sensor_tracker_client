from .connection import get_request, post_request_with_token, get_request_by_pk
from .decorator import cache_it
from .ResponseData import DataFactory

GET = "get"
POST = "post"
DELETE = "delete"
# PATCH = "patch"
PUT = "put"

API_METHOD_INFO = [
    {
        "name": "institution",
        "keyword": "institution/",
        "actions": [GET, POST]
    },
    {
        "keyword": "project",
        "actions": [GET, POST]
    },
    {
        "keyword": "manufacturer",
        "actions": [GET, POST]
    },
    {
        "keyword": "instrument",
        "actions": [GET, POST]
    },
    {
        "keyword": "instrument_on_platform",
        "actions": [GET, POST]
    },
    {
        "keyword": "sensor",
        "actions": [GET, POST]
    },
    {
        "keyword": "platform_type",
        "actions": [GET, POST]
    },
    {
        "keyword": "platform",
        "actions": [GET, POST]
    },
    {
        "keyword": "power",
        "actions": [GET, POST]
    },
    {
        "keyword": "deployment",
        "actions": [GET, POST]
    },
    {
        "keyword": "deployment_comment",
        "actions": [GET]
    },
    {
        "keyword": "platform_comment",
        "actions": [GET]
    },
    {
        "keyword": "sensor_on_instrument",
        "actions": [GET]
    }
]


def make_api_methods(sensor_tracker_api, api_info):
    for a in api_info:
        method_instance = api_method_factory(a)
        setattr(sensor_tracker_api, method_instance.__name__, method_instance)


class BaseAPIMethod:
    def __init__(self, api_info):
        self.api_key_word = api_info["keyword"]
        self._info = api_info

    def get(self, *args, **kwargs):
        if hasattr(self, "_get"):
            # todo or here?
            if args:
                payload = args[0]
                payload["format"] = 'json'

            else:
                payload = {"format": 'json'}
            args = (payload,)
            return self._get(self, *args, **kwargs)
        else:
            raise AttributeError("'{}' object has no attribute '{}'".format(self, 'get'))

    def post(self, *args, **kwargs):
        if hasattr(self, "_post"):
            return self._post(self, *args, **kwargs)
        else:
            raise AttributeError("'{}' object has no attribute '{}'".format(self.__name__, 'post'))

    def delete(self, *args, **kwargs):
        if hasattr(self, "_delete"):
            return self._delete(self, *args, **kwargs)
        else:
            raise AttributeError("'{}' object has no attribute '{}'".format(self, 'delete'))


def api_method_factory(api_info):
    method_name = api_info["name"] if "name" in api_info else api_info["keyword"]

    @cache_it(api_info["keyword"])
    def get(self, payload=None):
        # todo: make a input argument parser here?
        r = get_request(self.api_key_word, payload)
        return DataFactory(r).generate()

    def post(self, payload):
        return post_request_with_token(self.api_key_word, payload)

    i = BaseAPIMethod(api_info)
    i.__name__ = method_name
    for action in api_info["actions"]:
        if GET is action:
            setattr(i, "_" + GET, get)

        if POST is action:
            setattr(i, "_" + POST, post)

    return i
