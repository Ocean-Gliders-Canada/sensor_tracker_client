import json
from six.moves import urllib
from sensor_tracker_api.binder.binder import APIMethod


class APIPostMethod(APIMethod):
    def __init__(self, **kwargs):
        APIMethod.__init__(self, **kwargs)

    def post_deployment(self, content):
        post_type = "insert_deployment"
        res = self.post_content(post_type, content)
        return res

    def post_platform(self, content):
        post_type = "insert_platform"
        res = self.post_content(post_type, content)
        return res

    def post_project(self, content):
        post_type = "insert_project"
        res = self.post_content(post_type, content)
        return res

    def post_instrument_on_platform(self, content):
        post_type = "insert_instrument_on_platform"
        res = self.post_content(post_type, content)
        return res

    def post_platform_type(self, content):
        post_type = "insert_platform_type"
        res = self.post_content(post_type, content)
        return res

    def post_instrument(self, content):
        post_type = "insert_instrument"
        res = self.post_content(post_type, content)
        return res

    def post_sensor(self, content):
        post_type = "insert_sensor"
        res = self.post_content(post_type, content)
        return res

    def post_content(self, type, content):
        url = self.get_query_url(type)
        request = urllib.request.Request(url)
        request.add_header("Authorization", self.__get_auth_payload())
        try:
            ret = urllib.request.urlopen(request, self.__get_payload(content))
        except Exception as e:
            print(e)
            return None
        code = ret.getcode()
        res = False
        ret_data = ret.read()
        if code == 200:
            ret_dict = json.loads(ret_data)
            s = ret_dict.get("success", None)
            if s is not None:
                res = ret_dict.get("id", None)
            else:
                print(ret_data)
        else:
            print("error")
            print(ret_data)

        return res

    def __get_auth_payload(self):
        payload = "Token "
        payload = payload + self.token

        return payload

    def __get_payload(self, content):
        return urllib.parse.urlencode(content).encode("utf-8")


"""
p = APIPostMethod(host="http://127.0.0.1:8001/api/", token='1537ded79296862c889ffe368b9decc3b9c2afe1')
print(p.post_deployment(
    {"platform_name": "otn200", "deployment_number": 85, "institution_id": 1, "project_id": 1, "title": "85",
     "start_time": "2017-06-05 15:13:26", "platform_id": 2}))

"""
