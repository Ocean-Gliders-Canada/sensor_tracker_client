#!python
# coding=utf-8
from sensor_tracker_api.config.config import Config
from sensor_tracker_api.processor.get_process import Process
from sensor_tracker_api.checker.args_checker import InputChecker


class AccessApi(object):
    def __init__(self, debug=None, host=None, token=None, user=None, password=None):

        if debug:
            self.DEBUG = True
            self.SensorTackerApi = Config.SENSOR_TRACKER_LOCAL_URL
            if host:
                self.SensorTackerApi = host
        else:
            self.SensorTackerApi = Config.SENSOR_TRACKER_CONNECTOR
            self.DEBUG = False

        self.token = token
        self.user = user
        self.deployment_cache = {}
        self.password = password
        self.config = Config
        self.GLIDER_TYPES = self.config.GLIDER_TYPE
        self.process = Process(self.SensorTackerApi)
        self.arg_check = InputChecker(Config)

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
            raise TypeError("Incorrect deployment model input")
        self.arg_check = InputChecker(Config)

