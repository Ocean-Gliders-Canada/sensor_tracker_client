from sensor_tracker_api.object.meta_data import MetaData


class SimplyMetaDataFactory(object):
    def __init__(self, parser=None):
        self.parsers = parser

    def create(self, **kwargs):
        header = kwargs.pop("header", None)
        content = kwargs.pop("content", None)
        parser = kwargs.pop("parser", None)
        if parser:
            header, content = parser
        o = MetaData(header, content)
        return o

    def generate_obj(self, **kwargs):
        res = self.parse(**kwargs)
        return self.create(**res)

    def parse(self, **kwargs):
        res = self.parsers.parse(**kwargs)
        return res
