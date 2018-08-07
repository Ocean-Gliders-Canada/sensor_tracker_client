from sensor_tracker_api.object.meta_data import MetaData


class SimplyMetaDataFactory(object):


    @staticmethod
    def create(**kwargs):
        header = kwargs.pop("header",  None)
        content = kwargs.pop("content", None)
        parser = kwargs.pop("parser", None)
        if parser:
            header, content = parser
        o = MetaData(header, content)
        return o
