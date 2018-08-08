class Parser(object):
    def __init__(self):
        self.header = None

    def parse(self, **kwargs):
        df = kwargs.pop("df", None)
        df = df[0]
        header = self.__get_header(df)
        rows = self.__get_content(df)
        res = dict(
            header=header,
            content=rows,
        )
        return res

    def __get_header(self, df):
        if self.header is None:

            header = list(df.columns.values)
            for n in header:
                if "Unnamed" in n:
                    header.remove(n)
            self.header = header

        return self.header

    def __get_content(self, df):
        header = self.__get_header(df)
        subset = df[header]
        tuples = [tuple(x) for x in subset.values]
        return tuples
