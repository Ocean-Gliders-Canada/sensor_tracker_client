#!python
# coding=utf-8
from sensor_tracker_api.config import Config
from sensor_tracker_api.process import Process
from sensor_tracker_api.args_checker import InputChecker


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
            raise Exception("Incorrect deployment model input")
        self.arg_check = InputChecker(Config)

    def get_deployments(self, *args, **kwargs):
        """
        Input cloud be deployment number, or platform type or, platform name or platform name and start time

        :param specific:
        :param para:
        :return: relevant deployments data in pandas format
        """
        arg_type = kwargs.pop("arg_type", None)
        length_of_arg = len(args)
        if arg_type in self.config.ARG_TYPE:
            arg_type = self.config.ARG_TYPE[arg_type]
        else:
            arg_type = None
        if not arg_type:
            arg_type = self.arg_check.deployment_input_check(*args)

        res = None

        if arg_type == self.config.ARG_TYPE["INVALID"]:
            raise Exception("Invalid Input")
        elif arg_type == self.config.ARG_TYPE["general_model"]:
            res = self.process.get_deployments_by_general_model(*args)
        elif arg_type == self.config.ARG_TYPE["deployment_number"]:
            res = self.process.get_deployment_by_deployment_number(*args)
        elif arg_type == self.config.ARG_TYPE["model"]:
            res = self.process.get_platform_by_model(*args)
        elif arg_type == self.config.ARG_TYPE["platform_name"]:
            res = self.process.get_deployments_by_platform_name(*args)
        elif arg_type == self.config.ARG_TYPE["name_time"]:
            res = self.process.get_deployment_by_name_time(*args)

        return res

    def get_sensors(self, *args, **kwargs):
        arg_type = kwargs.pop("output", True)
        if arg_type:
            res = self.process.get_output_sensors_by_deployment(*args)
        else:
            res = self.process.get_sensors_on_deployment(*args)
        return res

    def get_instruments(self, *args, **kwargs):
        length_of_arg = len(args)
        res = None
        if length_of_arg == 1:
            name = args[0]
            res = self.process.get_instruments_on_platform_by_name(name)
        elif length_of_arg == 2:
            res = self.process.get_instrument_on_deployment(*args)
        return res

    def get_deployment_comments(self, platform_name, start_time):
        o = self.process.get_platform_deployment_comments(platform_name, start_time)
        return o

    def get_platform(self, *args, **kwargs):
        pass

    def __get_platform_by_model(self, model):
        return self.process.get_platform_by_model(model)

    def get_deployment_info(self, deployment_num):
        obj = self.process.get_deployment_by_deployment_number(deployment_num)
        data_dict = obj.to_dict()[0]
        platform_name = data_dict["platform_name"]
        start_time = data_dict['start_time']
        return platform_name, start_time

    def is_testing_mission(self, platform_name, start_time):
        obj = self.get_deployments(platform_name, start_time)
        res = obj.get_column("testing_mission")
        testing = res[0]
        if not testing:
            testing = False
        return testing

    def get_mission_id(self, platform_name, start_time):
        obj = self.get_deployments(platform_name, start_time)
        res = obj.get_column("deployment_number")
        num = res[0]
        return num

"""
a = AccessApi(debug=True)
b = a.get_deployments("slocum")
print(b.to_dict())
b.to_csv("/Users/xiang/Desktop/output/3.csv")
"""