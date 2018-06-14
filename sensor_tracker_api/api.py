#!python
# coding=utf-8
import logging
from sensor_tracker_api.config import Config
from sensor_tracker_api.process import Process

logger = logging.getLogger(__name__)


class AccessApi(object):
    def __init__(self, debug=None, token=None, user=None, password=None):

        if debug:
            self.DEBUG = True
            self.SensorTackerApi = Config.SENSOR_TRACKER_LOCAL_URL
        else:
            self.SensorTackerApi = Config.SENSOR_TRACKER_CONNECTOR
            self.DEBUG = False

        self.token = token
        self.user = user
        self.deployment_cache = {}
        self.password = password
        self.GLIDER_TYPES = Config.GLIDER_TYPE
        self.process = Process(self.SensorTackerApi)

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
        if type(models) is list:
            self.GLIDER_TYPES = models
        elif type(models) is str:
            self.GLIDER_TYPES = [models]
        else:
            raise Exception("Incorrect deployment model input")

    def __init_deployment_cache(self):
        glider_models = Config.GLIDER_TYPE
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

    def get_sensors_on_deployment(self, platform_name, start_time):
        df = self.process.get_sensors_on_deployment(platform_name, start_time)
        return df

    def get_output_sensors(self, platform_name, start_time):
        df = self.process.get_output_sensors_by_deployment(platform_name, start_time)
        return df

    def get_deployments(self, para, specific=None):
        """
        para cloud be deployment number, or platform type or, platform name.

        :param specific:
        :param para:
        :return: relevant deployments data in pandas format
        """
        pass

    def get_deployments_by_general_model(self, general_model):
        return self.process.get_deployments_by_general_model(general_model)

    def get_deployment_by_deployment_number(self, number):
        return self.process.get_deployment_by_deployment_number(number)

    def get_deployments_by_platform_name(self, platform_name):
        return self.process.get_deployments_by_platform_name(platform_name)

    def get_platform_by_model(self, model):
        return self.process.get_platform_by_model(model)

    def get_platform_deployment(self, platform_name, start_time):
        return self.process.get_deployment_by_name_time(platform_name, start_time)

    def get_deployment_instruments(self, platform_name, start_time):
        return self.process.get_instrument_on_deployment(platform_name, start_time)

    def get_sensor_on_instruments(self, instrument_identifier):
        pass

    def get_instruments_id(self, identifier):
        pass

    def get_instruments_on_platform(self, platform_name, time, instrument_identifier):
        pass

    def get_platform_deployment_comments(self, platform_name, start_time):

        pass

    def get_platform_type(self, model_name):
        pass

    def get_manufacturer(self, id):
        pass

    def get_deployment_number(self, platform_name, start_time):
        pass

    def get_deployment_info(self, deployment_num):
        df = self.process.get_deployment_by_deployment_number(deployment_num)
        data_dict = df.to_dict('records')[0]
        platform_name = data_dict["platform_name"]
        start_time = data_dict['start_time']
        return platform_name, start_time

    def get_mission_end_time(self, platform_name, start_time):
        pass


a = AccessApi(debug=True)
print(a.get_deployment_info(1))
