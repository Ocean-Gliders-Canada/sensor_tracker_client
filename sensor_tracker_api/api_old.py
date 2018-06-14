#!python
# coding=utf-8
import json, requests, logging

from six.moves import urllib

logger = logging.getLogger(__name__)


class Config(object):
    # This is default api link
    SENSOR_TRACKER_CONNECTOR = 'http://bugs.ocean.dal.ca/sensor_tracker/api/'
    SENSOR_TRACKER_LOCAL_URL = "http://127.0.0.1:8000/api/"
    GLIDER_MODELS = ["Wave", "Slocum"]


class AccessApi(object):
    def __init__(self, debug=None):

        if debug:
            self.DEBUG = True
            self.SensorTackerApi = Config.SENSOR_TRACKER_LOCAL_URL
        else:
            self.SensorTackerApi = Config.SENSOR_TRACKER_CONNECTOR
            self.DEBUG = False

        self.token = None
        self.user = None
        self.deployment_cache = {}
        self.password = None
        self.GLIDER_MODELS = Config.GLIDER_MODELS

    def check_auth(self):
        if not self.token:
            raise Exception("Provide authentication token or Provide (username, password), before use insert methods")

    def set_authentication(self, content):
        if type(content) is str:
            self.token = content
        elif type(content) is tuple:
            self.user = content[0]
            self.password = content[1]
        else:
            raise Exception("Either provide token string or user name and passowrd in format ('username', 'password')")
        # Todo: create check token methods

    def set_deplopyment_model(self, models):
        self.GLIDER_MODELS = models

    def __init_deployment_cache(self):
        glider_models = Config.GLIDER_MODELS
        deployment_list = []

        for model in glider_models:
            deployment_list.extend(self.get_deployments(model))

        for deployment in deployment_list:
            self.deployment_cache[deployment["deployment_number"]] = {"platform_name": 1, "start_time": 2,
                                                                      "end_time": 3}

    def set_deployment_number(self, num):
        # Todo: Write the method to check the update
        if type(num) is int:
            deployemnt_number = num
        elif type(num) is str:
            try:
                deployemnt_number = int(num)
            except ValueError:
                raise Exception("Deployment number is Integer")
        else:
            raise Exception("Deployment number is Integer")

        if num in self.deployment_cache:
            return self.deployment_cache[num]
        else:
            raise Exception("invalid deployment")

    def get_sensors_on_platform(self, platform_name, start_time):
        instrument = self.get_deployment_instruments(platform_name, start_time)

        sensor_array = []

        for i in instrument:
            sensor = self.__parse_content("get_sensors", {"instrument_id": i["instrument"]["id"]})
            sensor_array.extend(sensor)

        if self.DEBUG:
            logger.warning("get_sensors result {} ".format(sensor_array))
        return sensor_array

    def get_output_sensors(self, platform_name, start_time):
        instrument = self.get_deployment_instruments(platform_name, start_time)

        sensor_array = []

        for i in instrument:
            sensor = self.__parse_content("get_output_sensors", {"id": i["instrument"]["id"]})
            sensor_array.extend(sensor)

        if self.DEBUG:
            logger.warning("get_output_sensors result {} ".format(sensor_array))
        return sensor_array

    def get_deployments(self, model_name):
        platform_type = self.get_platform_type(model_name)

        result = []

        for i in platform_type:
            result.extend(self.__parse_content("get_deployments/", {"platform__platform_type__model": i}))

        if self.DEBUG:
            logger.warning("get_deployments result {} ".format(result))

        return result

    def get_platform_by_type(self, model):
        result = self.__parse_content("get_platform_deployments", {"model": model})

        return result

    def get_platform_deployment(self, platform_name, start_time):

        result = self.__parse_content("get_platform_deployments", {"name": platform_name, "time": start_time})

        if self.DEBUG:
            logger.warning("get_platform_deployment result {} ".format(result))

        return result

    def get_instruments(self, instrument_identifier):

        result = self.__parse_content("get_instruments", {"identifier": instrument_identifier})

        return result

    def get_sensor_on_instruments(self, instrument_identifier):
        instrument_id = self.get_instruments_id(instrument_identifier)
        result = self.__parse_content("get_sensors", {"instrument_id": instrument_id})

        return result

    def get_instruments_id(self, identifier):
        instruments = self.__parse_content("get_instruments")
        id = -1

        for x in instruments:
            if identifier == x["identifier"]:
                id = x["id"]
        if identifier:
            return id
        else:
            return instruments

    def get_instruments_on_platform(self, platform_name, time, instrument_identifier):
        instruments_on_platform = self.__parse_content("get_instruments_on_platform",
                                                       {"name": platform_name, "time": time,
                                                        "identifier": instrument_identifier})
        return instruments_on_platform

    def get_platform_deployment_comments(self, platform_name, start_time):

        result = self.__parse_content("get_platform_deployment_comments", {"name": platform_name, "time": start_time})

        if self.DEBUG:
            logger.warning("get_platform_deployment result {} ".format(result))

        return result

    def get_deployment_instruments(self, platform_name, start_time):

        result = self.__parse_content("get_deployment_instruments", {"name": platform_name, "time": start_time})
        if self.DEBUG:
            logger.warning("get_deployment_instruments result {} ".format(result))
        return result

    def get_platform_id(self, platform_name):
        platform = self.__parse_content("get_platform")
        platform_id = -1
        for x in platform:
            if x['name'] == platform_name:
                platform_id = x['id']
                return platform_id
        return platform_id

    def get_platform_type(self, model_name):
        platform_type = self.__parse_content("get_platform_type")

        name_list = []

        for item in platform_type:
            if model_name.lower() in item['model'].lower():
                name_list.append(item['model'])

        if self.DEBUG:
            logger.warning("get_platform_type result {} ".format(name_list))
        return name_list

    def get_manufacturer(self, id):
        result = self.__parse_content("get_manufacturer", {"id": id})

        if self.DEBUG:
            logger.warning("get_manufacturer result {} ".format(result))

        return result

    def get_mission_id(self, platform_name, start_time):
        result = self.get_platform_deployment(platform_name, start_time)
        result = result[0]['title']
        if self.DEBUG:
            logger.warning("get_mission_id result {} ".format(result))

        return result

    def get_mission_info(self, mission_id):
        deps = self.get_deployments("Wave")
        deps.extend(self.get_deployments("Slocum"))
        platform_name = None
        start_time = None
        for x in deps:
            if x["title"] == str(mission_id):
                platform_name = x["platform"]["name"]
                start_time = x["start_time"]

        return platform_name, start_time

    def get_mission_end_time(self, platform_name, start_time):
        result = self.get_platform_deployment(platform_name, start_time)
        result = result[0]['end_time']
        if self.DEBUG:
            logger.warning("get_mission_end_time result {} ".format(result))

        return result

    def is_testing_mission(self, platform_name, start_time):

        result = self.get_platform_deployment(platform_name, start_time)
        if result[0]['testing_mission']:
            result = True
        else:
            return False

        if self.DEBUG:
            logger.warning("is_testing_mission result {} ".format(result))

        return result

    # Below is for the insert functions
    def insert_instrument(self, identifier, short_name, **kwargs):
        self.check_auth()
        l = {"identifier": identifier, "short_name": short_name}

        if self.get_instruments(identifier):
            print("Instrument %s is already exist in database" % identifier)
        else:
            long_name = kwargs.pop('long_name', False)
            if long_name:
                l["long_name"] = kwargs.pop('long_name', False)
            manufacturer_id = kwargs.pop('manufacturer_id', False)
            if manufacturer_id:
                l["manufacturer_id"] = kwargs.pop('manufacturer_id', False)
            serial = kwargs.pop('serial', False)
            if serial:
                l["serial"] = kwargs.pop('serial', False)
            instrument_id = kwargs.pop('instrument_id', False)
            if instrument_id:
                l["instrument_id"] = kwargs.pop('instrument_id', False)
            l["comment"] = kwargs.pop('comment', "Auto generate")

            self.post_content("insert_instrument", l)

    def insert_instrument_on_platform(self, instrument, platform, starttime, **kwargs):
        self.check_auth()
        instrument_id = self.get_instruments_id(instrument)
        platform_id = self.get_platform_id(platform)

        if instrument_id != -1 and platform_id != -1:

            l = {"instrument_id": instrument_id, "platform_id": platform_id, "start_time": starttime}
            end_time = kwargs.pop('end_time', False)
            comment = kwargs.pop('comment', "Auto generate")
            if end_time:
                l["end_time"] = end_time
            l["comment"] = comment

            if self.get_instruments_on_platform(platform, starttime, instrument):
                print("instrument: %s exist on platform %s already on time %s" % (instrument, platform, starttime))
            else:
                self.post_content("insert_instrument_on_platform", l)
        else:
            print("invalid instrument: %s , id: %d or platform %s , id: %d" % (
                instrument, instrument_id, platform, platform_id))

    def insert_sensor(self, instrument_identifier, sensor_identifier, **kwargs):
        self.check_auth()

        def sensor_is_on_instrument(instrument_identifier, sensor_identifier):
            sensors = self.get_sensor_on_instruments(instrument_identifier)
            for s in sensors:
                if s['identifier'] == sensor_identifier:
                    return True
            return False

        instrument_id = self.get_instruments_id(instrument_identifier)

        long_name = kwargs.pop('long_name', False)
        standard_name = kwargs.pop('standard_name', False)
        type = kwargs.pop('type', False)
        units = kwargs.pop('units', False)
        precision = kwargs.pop('precision', False)
        accuracy = kwargs.pop('accuracy', False)
        resolution = kwargs.pop('resolution', False)
        valid_min = kwargs.pop('valid_min', False)
        valid_max = kwargs.pop('valid_max', False)
        include_in_output = kwargs.pop('include_in_output', True)
        display_in_web_interface = kwargs.pop('display_in_web_interface', False)
        comment = kwargs.pop('comment', "Auto generate")

        if instrument_id == -1:
            print("instrument identifier: %s is invalid" % instrument_identifier)
        else:

            if sensor_is_on_instrument(instrument_identifier, sensor_identifier):
                print("sensor: %s is already exist on the instrument %s)" % (sensor_identifier, instrument_identifier))
            else:
                l = {"instrument_id": instrument_id, "identifier": sensor_identifier}

                if long_name:
                    l["long_name"] = long_name

                if standard_name:
                    l["standard_name"] = standard_name

                if type:
                    l["type"] = type

                if units:
                    l["units"] = units

                if precision:
                    l["precision"] = precision

                if accuracy:
                    l["accuracy"] = accuracy

                if resolution:
                    l["resolution"] = resolution

                if valid_min:
                    l["valid_min"] = valid_min

                if valid_max:
                    l["valid_max"] = valid_max

                if include_in_output:
                    l["include_in_output"] = include_in_output

                if display_in_web_interface:
                    l["display_in_web_interface"] = display_in_web_interface

                if comment:
                    l["comment"] = comment

                self.post_content("insert_sensor", l)

    def post_content(self, type, data):
        url = self.__get_query_url(type, arguments=None)

        if url[-1] != "/":
            url = url + "/"

        session_request = requests.session()

        if not self.token:
            if "token" in PAYLOAD and PAYLOAD["token"]:
                self.token = PAYLOAD["token"]
            else:
                payload = {
                    "username": PAYLOAD["username"],
                    "password": PAYLOAD["password"]
                }
                url_token = 'http://127.0.0.1:8000/api/get_token/'
                r = requests.post(url_token, data=payload)
                self.token = json.loads(r.text)["token"]

        session_request.post(
            url,
            data=data,
            headers={
                "Authorization": "Token " + self.token
            }
        )

    def __parse_content(self, type, arguments=None):
        url = self.__get_query_url(type, arguments)

        if self.DEBUG:
            logger.warning("get url {} ".format(url))
        return self.__get_content(url)


    def parse_content(self, type, arguments=None):
        url = self.__get_query_url(type, arguments)

        if self.DEBUG:
            logger.warning("get url {} ".format(url))
        return self.__get_content(url)

    def __get_content(self, url):
        r = requests.get(url)
        if r.status_code == 200:
            return r.json()['data']
        return None

    def __get_query_url(self, type, arguments=None):
        if arguments is None:
            return self.SensorTackerApi + type
        else:
            return self.SensorTackerApi + type + '?' + urllib.parse.urlencode(arguments)

    def validate_args(self, *args):
        raise NotImplemented

    def remove_null_value(self, dict):
        for i, j in dict:
            if j is False:
                del dict[i]

        return dict


api = AccessApi(debug=True)
# b = api.get_platform_deployment("Fundy", "2018-05-17 16:02:26")
# b = api.get_platform_type("Slocum")
# print(b)
# platform_type = api.parse_content("get_platform_type", {"model": "Slocum Glider G2"})
#test = api.parse_content("get_platform", {"type":"Slocum Glider G3"})
# print(test)

# test = api.get_deployment_instruments("dal556", "2017-06-05 15:13:26")
#est = api.get_deployment_instruments("dal556", "2017-06-05 15:13:26")
test = api.parse_content("get_manufacturer",{})
print(test)
#print(test)
