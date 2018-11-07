from sensor_tracker_api.parser.json_parser import Parser


class JsonIdPaser(Parser):

    def parse(self, **kwargs):
        pattern = kwargs.pop("pattern", None)
        content = kwargs.pop("content", None)
        if pattern:
            pattern = [('id',)] + pattern

        param = dict(
            pattern=pattern,
            content=content
        )
        return super(JsonIdPaser, self).parse(**param)
