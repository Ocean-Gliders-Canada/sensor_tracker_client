from six.moves import urllib
import requests


class APIGetMethod(object):
    def __init__(self, **kwargs):
        self.host = kwargs.pop("host")

    def get_platform_deployments(self, **kwargs):
        platform_name = kwargs.pop("platform_name", None)
        start_time = kwargs.pop("start_time", None)
        deployment_number = kwargs.pop("deployment_number", None)
        if platform_name and start_time:
            result = self.__parse_content("get_platform_deployments", {"name": platform_name, "time": start_time})
        elif platform_name:
            result = self.__parse_content("get_platform_deployments", {"name": platform_name})
        elif deployment_number:
            result = self.__parse_content("get_platform_deployments", {"deployment_number": str(deployment_number)})
        else:
            result = self.__parse_content("get_platform_deployments")

        return result

    def get_instruments(self, **kwargs):
        instrument_identifier = kwargs.pop("instrument_identifier", None)
        instrument_id = kwargs.pop("instrument_id", None)
        instrument_serial = kwargs.pop("serial", None)
        param = {}
        if instrument_id:
            param["id"] = instrument_id
            result = self.__parse_content("get_instruments", param)
        elif instrument_identifier or instrument_serial:
            param = {}
            if instrument_identifier:
                param["identifier"] = instrument_identifier
            if instrument_serial:
                param["serial"] = instrument_serial
            result = self.__parse_content("get_instruments", param)
        else:
            result = self.__parse_content("get_instruments")
        return result

    def get_deployment_instruments(self, **kwargs):
        platform_name = kwargs.pop("platform_name", None)
        start_time = kwargs.pop("start_time", None)

        result = self.__parse_content("get_deployment_instruments", {"name": platform_name, "time": start_time})
        return result

    def get_sensors(self, **kwargs):
        instrument_id = kwargs.pop("instrument_id", None)
        if instrument_id:
            result = self.__parse_content("get_sensors", {"instrument_id": instrument_id})
        else:
            result = self.__parse_content("get_sensors")
        return result

    def get_output_sensors(self, **kwargs):
        """
        Get output sensor
        :param kwargs:
        :return:
        """
        instrument_identifier = kwargs.pop("instrument_identifier", None)
        instrument_id = kwargs.pop("instrument_id", None)
        para = {}
        if instrument_identifier:
            para["identifier"] = instrument_identifier
        elif instrument_id:
            para["id"] = instrument_id

        result = self.__parse_content("get_output_sensors", para)

        return result

    def get_platform_type(self, **kwargs):
        model = kwargs.pop("model", None)
        name = kwargs.pop("name", None)
        para = {}
        if model:
            para["model"] = model
        elif name:
            para["name"] = name

        result = self.__parse_content("get_platform_type", para)
        return result

    def get_platform(self, **kwargs):
        platform_id = kwargs.pop("platform_id", None)
        platform_name = kwargs.pop("platform_name", None)
        platform_type = kwargs.pop("platform_type", None)

        para = {}
        if platform_type:
            para["type"] = platform_type
        if platform_name:
            para["name"] = platform_name
        elif platform_id:
            para["id"] = platform_id

        result = self.__parse_content("get_platform", para)

        return result

    def get_manufacturer(self, **kwargs):
        manufacturer_id = kwargs.pop("manufacturer_id", None)
        manufacturer_name = kwargs.pop("manufacturer_name", None)
        para = {}
        if manufacturer_id:
            para["id"] = manufacturer_id
        elif manufacturer_name:
            para["name"] = manufacturer_name

        result = self.__parse_content("get_platform", para)

        return result

    def __parse_content(self, api_type, arguments=None):
        if not arguments:
            arguments = None
        url = self.__get_query_url(api_type, arguments)

        return self.__get_content(url)

    def __get_content(self, url):
        r = requests.get(url)
        if r.status_code == 200:
            return r.json()['data']
        return None

    def __get_query_url(self, type, arguments=None):
        if arguments is None:
            return self.host + type
        else:
            return self.host + type + '?' + urllib.parse.urlencode(arguments)
