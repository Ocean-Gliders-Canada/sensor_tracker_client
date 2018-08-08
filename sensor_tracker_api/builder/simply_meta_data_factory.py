from sensor_tracker_api.object.meta_data import MetaData


class SimplyMetaDataFactory(object):
    def __init__(self, parser):
        self.parsers = parser

    def create(self, **kwargs):
        header = kwargs.pop("header", None)
        content = kwargs.pop("content", None)
        parser = kwargs.pop("parser", None)
        if parser:
            header, content = parser
        o = MetaData(header, content)
        return o

    def generate_obj(self, content_format, content):
        header, rows = self.parse(content_format, content)
        return self.create(header=header, content=rows)

    def parse(self, content_format, content):
        header, rows = self.parsers.parse(content_format, content)
        return header, rows
