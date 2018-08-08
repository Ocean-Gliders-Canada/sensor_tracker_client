from sensor_tracker_api.parser.parser import Parser as p


class Parser(p):

    def parse(self, **kwargs):
        pattern = kwargs.pop("pattern", None)
        content = kwargs.pop("content", None)
        rows = self.__parser(pattern, content)
        header = self.create_pandas_header(pattern)
        res = dict(
            header=header,
            content=rows,
        )
        return res

    def __parser(self, pattern, content):
        table_rows = []
        for item in content:
            row = self.row_parser(pattern, item)
            table_rows.append(row)
        return table_rows

    def row_parser(self, format, item):
        row = ()
        for i in format:
            res = self.get_content(i, item)
            row = row + (res,)

        return row

    def get_content(self, format, item):
        res = None
        for x in format:
            if item and x in item:
                res = item[x]
            item = res

        return res

    def create_pandas_header(self, format):
        header = []
        for x in format:
            name = self.get_name(x)
            header.append(name)
        return header

    def get_name(self, item):
        length = len(item)
        name = "Unknow"
        if length >= 1:
            name = item[0]

        for index in range(1, length):
            name = name + "__" + item[index]

        return name
