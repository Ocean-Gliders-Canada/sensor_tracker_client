import requests

from six.moves import urllib


class APIMethod(object):
    def __init__(self, **kwargs):
        self.host = kwargs.pop("host", None)
        self.token = kwargs.pop("token", None)

    def parse_content(self, api_type, arguments=None):
        if not arguments:
            arguments = None
        url = self.get_query_url(api_type, arguments)

        return self.get_content(url)

    def get_content(self, url):
        try:
            r = requests.get(url)
        except Exception as e:
            print(e)
            return None
        if r.status_code == 200:
            return r.json()['data']
        return None

    def get_query_url(self, type, arguments=None):
        if arguments is None:
            res = self.host + type
            if not res.endswith('/'):
                res = res + '/'
            return res
        else:
            return self.host + type + '?' + urllib.parse.urlencode(arguments)

# p = APIGetMethod(host="http://127.0.0.1:8000/api/")
# print(p.get_output_sensors_by_platform("dal556", "2017-06-05 15:13:26"))
# ob = p.get_deployments_by_general_model("slocum")
# print(ob.to_dict())
# print(p.get_platform_deployment_comments(platform_name="dal556", start_time="2017-06-05 15:13:26"))
