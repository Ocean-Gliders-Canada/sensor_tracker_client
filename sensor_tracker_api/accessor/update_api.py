from sensor_tracker_api.accessor.api import AccessApi
from sensor_tracker_api.processor.update_process import UpdateProcess


class UpdateApi(AccessApi):
    def __init__(self, **kwargs):

        self.path = kwargs.pop("path", None)
        AccessApi.__init__(self, **kwargs)
        self.user = kwargs.pop("user", None)
        self.password = kwargs.pop("password", None)
        self.process = UpdateProcess(self.path, self.SensorTackerHost, self.token)

    def update_deployment(self, *args, **kwargs):
        self.process.update_deployment()

    def update_instrument(self, *args, **kwargs):
        raise NotImplementedError

    def update_sensor(self, *args, **kwargs):
        raise NotImplementedError
