from sensor_tracker_api.reader.data_reader import DataReader
from sensor_tracker_api.binder.update_binder import APIUpdateMethod


class PostProcess(object):
    def __init__(self, path, host, token):
        self.reader = DataReader(path)
        self.host = host
        self.token = token
        self.binder = APIUpdateMethod(host=self.host, token=self.token)
        self.obj = self.reader.generate_obj()

    def post_deployment(self, *args, **kwargs):
        self.binder.post_deployment(kwargs)

    def post_sensor(self):
        print("no thing will happen")

    def _foreignKey_id_replace(self):
        pass

