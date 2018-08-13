from sensor_tracker_api.accessor import *


class AccessApi(object):
    def __init__(self, **kwargs):
        self.debug = kwargs.pop("debug", None)
        self.host = kwargs.pop("host", None)
        self.token = kwargs.pop("token", None)
        self.user = kwargs.pop("user", None)
        self.password = kwargs.pop("password", None)
        self.get_api = None
        self.update_api = None

    def get_deployments(self, *args, **kwargs):
        self._init_get_api()
        return self.get_api.get_deployments(*args, **kwargs)

    def get_sensors(self, *args, **kwargs):
        self._init_get_api()
        return self.get_api.get_sensors(*args, **kwargs)

    def get_instruments(self, *args, **kwargs):
        self._init_get_api()
        return self.get_api.get_instruments(*args, **kwargs)

    def get_deployment_comments(self, *args, **kwargs):
        self._init_get_api()
        return self.get_api.get_deployment_comments(*args, **kwargs)

    def get_platform(self, *args, **kwargs):
        self._init_get_api()
        return self.get_api.get_platform(*args, **kwargs)

    def get_deployment_info(self, deployment_num):
        self._init_get_api()
        return self.get_api.get_deployment_info(deployment_num)

    def is_testing_mission(self, platform_name, start_time):
        self._init_get_api()
        return self.get_api.get_mission_id(platform_name, start_time)

    def get_mission_id(self, platform_name, start_time):
        self._init_get_api()
        return self.get_api.get_mission_id(platform_name, start_time)

    def update_deployment(self, path):
        self._init_update_api(path)
        return self.update_api.update_deployment()

    def __dict__(self):
        res = dict(
            debug=self.debug,
            host=self.host,
            token=self.token,
            user=self.user,
            password=self.password
        )
        return res

    def _init_get_api(self):
        if self.get_api is None:
            self.get_api = GetApi(**self.__dict__())

    def _init_update_api(self, path):
        param = {"path": path}
        param = {**param, **self.__dict__()}
        self.update_api = UpdateApi(**param)


"""
a = AccessApi(debug=True)
b = a.get_deployments("Fundy", "2018-05-17 16:02:26")
print(b.to_csv("/Users/xiang/Desktop/output/deployment.csv"))
#a.update_deployment("asd")
"""