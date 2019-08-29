from . import basic_setting as default_setting


class Setting(object):

    def __init__(self):
        for setting in dir(default_setting):
            if setting.isupper():
                setattr(self, setting, getattr(default_setting, setting))

    @property
    def HOST_URL(self):
        if self.DEBUG:
            return self.DEBUG_HOST
        else:
            return self.HOST

    @property
    def DEBUG_HOST(self):
        return self._DEBUG_HOST

    @DEBUG_HOST.setter
    def DEBUG_HOST(self, url):
        if not url.endswith("/"):
            url = url + "/"
        self._DEBUG_HOST = url
