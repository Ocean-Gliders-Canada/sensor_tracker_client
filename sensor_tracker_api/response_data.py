import json
import requests


class Datum:
    def __init__(self, raw_data, status_code):
        self.raw = raw_data
        self.status_code = status_code


class ResponseData:
    def __init__(self):
        self._raw = []
        self.pages = False

    @property
    def raw(self):
        return self._raw

    @raw.setter
    def raw(self, value):
        self._raw.append(value)

    @property
    def dict(self):
        if not hasattr(self, "_dict"):
            self._dict = []
            for a in self.raw:
                status_code, data = a
                if status_code == 200:
                    self._dict.extend(data["results"])
        return self._dict

    @property
    def json(self):
        return json.dumps(self.dict)


class DataFactory:
    def __init__(self, response):
        self.response = response

    def generate(self):
        new_data = ResponseData()
        response_json = self.response.json()
        new_data.raw = (self.response.status_code, response_json)
        if response_json["next"]:
            new_data.pages = True
            self._generate(response_json["next"], new_data)
        return new_data

    def _generate(self, url, data_obj):
        response = requests.get(url)
        response_json = response.json()
        data_obj.raw = (self.response.status_code, response_json)
        if response_json["next"]:
            self._generate(response_json["next"], data_obj)
        return data_obj