from sensor_tracker_api.processor.post_process import PostProcess
from sensor_tracker_api.binder.update_binder import APIUpdateMethod
from sensor_tracker_api.parser.json_parser import Parser
from sensor_tracker_api.config.config import Config
from sensor_tracker_api.utilities.list_compare import compare_list
from sensor_tracker_api.processor.get_process import BaseGetProcess


class UpdateProcess(PostProcess):
    def __init__(self, path, host, token):
        PostProcess.__init__(self, path, host, token)
        self.new_header = None

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

        diff_value, new_value = self.__exist_check(content_type)
        diff_value, new_value, new_headers = self.__header_content_transform(content_type, diff_value, new_value)
        if new_value:
            for item in new_value:
                value = self.__generate_value(new_headers, item)
                method = post_prefix + content_type
                self.__callMethod(method, value)
        if diff_value:
            for item in diff_value:
                method = update_prefix + content_type
                self.__callMethod(method, param=item)

    def _update_deployment(self, ids, content):
        method = 'update_deployment'
        param = [ids, content]
        self._update_method(method, param)

    def __generate_value(self, header, content):
        ret = {}
        l = len(header)
        for x in range(0, l):
            ret[header[x]] = content[x]

        return ret

    def _update_sensor(self, ids):
        method = 'update_sensor'
        param = [ids, self.obj]
        self._update_method(method, param)

    def _update_method(self, method, param):
        update_binder = APIUpdateMethod(host=self.host, token=self.token)
        self.__callMethod(method, param=param, o=update_binder)

    def __callMethod(self, name, param=None, o=None):
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
        suffix = "_format"
        header_type = header_type + suffix
        header_format = Config.FORMAT[header_type]
        header = Parser().create_pandas_header(header_format)
        file_header = self.obj.header
        return compare_list(header, file_header)

    def __value_type_check(self, checker_type):
        """
        To be implement, the purpose of this method is check the value
        of type. If types are correct then return true, otherwise return false
        """
        return True

    def __exist_check(self, check_type):
        """
        if exist return the Ids,
        if not exist then return None
        also modified the obj, since if it is the same, then it doesn't need to do anything to it.
        :param check_type:
        :return:
        """
        unique_variable = Config.SEARCH_KEY[check_type]
        search_key_index = []
        file_header = self.obj.header
        for x in unique_variable:
            i = file_header.index(x)
            search_key_index.append(i)

        contents = self.obj.content
        diff_index = []
        new_index = []
        l = len(contents)
        for i in range(0, l):
            keys = []
            content = contents[i]
            for x in search_key_index:
                keys.append(content[x])
            ret = self.__get_content(keys, check_type)
            empty = False
            if ret:
                try:
                    value = ret.content[0]
                    if not compare_list(content, value):
                        diff_index.append(content)
                except IndexError:
                    empty = True
            if not ret or empty:
                new_index.append(content)

        return diff_index, new_index

    def __get_content(self, key, content_type):
        res = None
        base_get = BaseGetProcess(self.host)
        if content_type == "deployment":
            try:
                res = base_get.get_deployment_by_name_time(*key)
            except Exception as e:
                print(e)
                pass
        return res

    def __delete_exist_no_change(self, id):
        return None

    def __header_content_transform(self, content_type, diff_value, new_value):
        content_type = content_type
        replacement_header = Config.REPLACEMENT_VARIABLE[content_type]
        new_diff_value = []
        new_new_value = []
        new_headers = self._create_new_header(replacement_header, self.obj.header)
        get_process = BaseGetProcess(self.host)
        for value in diff_value:
            temp_value = self.__transform(content_type, self.obj.header, value, get_process)
            new_diff_value.append(temp_value)

        for value in new_value:
            temp_value = self.__transform(content_type, self.obj.header, value, get_process)
            new_new_value.append(temp_value)

        return new_diff_value, new_new_value, new_headers

    def __transform(self, content_type, headers, content, get_process):
        new_content = []
        l = len(headers)
        content_type_info = Config.REPLACEMENT_VARIABLE[content_type]

        for index in range(0, l):
            header = headers[index]
            if header in content_type_info:
                method = content_type_info[header][1]
                search_key = self.__find_search_key(header, self.obj.header, content)
                new_item = self.__callMethod(method, param=search_key, o=get_process)
                new_content.append(new_item)
            else:
                new_content.append(content[index])

        return new_content

    def __find_search_key(self, key_name, header, content):
        l = len(header)
        for index in range(0, l):
            if key_name == header[index]:
                return content[index]

    def _create_new_header(self, content_type_info, headers):
        new_header = []
        for header in headers:
            if header in content_type_info:
                new_header.append(content_type_info[header][0])
            else:
                new_header.append(header)

        return new_header


a = UpdateProcess('/Users/xiang/Desktop/output/deployment.csv', host="http://127.0.0.1:8001/api/",
                  token='1537ded79296862c889ffe368b9decc3b9c2afe1')
a.update_deployment()
