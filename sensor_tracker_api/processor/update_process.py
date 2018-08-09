from sensor_tracker_api.processor.post_process import PostProcess
from sensor_tracker_api.binder.update_binder import APIUpdateMethod


class UpdateProcess(PostProcess):
    def __init__(self, path, host, token):
        PostProcess.__init__(self, path, host, token)

    def update_deployment(self):
        content_type = "deployment"
        self.__update(content_type)

    def update_sensor(self):
        content_type = "sensor"
        self.__update(content_type)

    def __update(self, content_type):
        post_prefix = 'post_'
        update_prefix = '_update_'
        content_type = content_type
        header_checker_res = self.__header_check(content_type)
        if not header_checker_res:
            raise ValueError("The dataframe header doesn't meet requirement")
        value_check_res = self.__value_type_check(content_type)
        if not value_check_res:
            raise ValueError("The dataframe header doesn't meet requirement")

        exist_res = self.__exist_check(content_type)
        if exist_res is False:
            method = post_prefix + content_type
            self.__callMethod(method)
        else:
            method = update_prefix + content_type
            self.__callMethod(method, param=exist_res)

    def _update_deployment(self, ids):
        method = 'update_deployment'
        param = [ids, self.obj]
        self._update_method(method, param)

    def _update_sensor(self, ids):
        method = 'update_sensor'
        param = [ids, self.obj]
        self._update_method(method, param)

    def _update_method(self, method, param):
        update_binder = APIUpdateMethod(host=self.host, token=self.token)
        self.__callMethod(method, param=param, o=update_binder)

    def __callMethod(self, name, param=None, o=None):
        res = None
        obj = self
        if o:
            obj = o
        if param:
            if type(param) is dict:
                res = getattr(obj, name)(**param)
            elif type(param) is list:
                res = getattr(obj, name)(*param)
            else:
                res = getattr(obj, name)(param)
        else:
            res = getattr(obj, name)()

        return res

    def __header_check(self, header_type):
        return True

    def __value_type_check(self, checker_type):
        return True

    def __exist_check(self, check_type):
        """
        if exist return the Ids,
        if not exist then return None
        also modified the obj, since if it is the same, then it doesn't need to do anything to it.
        :param check_type:
        :return:
        """
        return True

    def __delete_exist_no_change(self, id):
        return None


a = UpdateProcess('/Users/xiang/Desktop/output/deployment.csv', host="http://127.0.0.1:8001/api/",
                  token='1537ded79296862c889ffe368b9decc3b9c2afe1')
a.update_deployment()
