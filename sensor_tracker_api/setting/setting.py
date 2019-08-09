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
