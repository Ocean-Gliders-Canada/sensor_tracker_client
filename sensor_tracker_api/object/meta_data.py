import pandas as pd


class MetaData(object):
    def __init__(self, header, content):
        # []
        self.header = header
        # [(),(),]
        self.content = content

    def add(self, row):
        type_of_input = type(row)
        if type_of_input is tuple:
            self.content.append(row)
        elif type_of_input is MetaData:
            self.content.extend(row.content)

    def remove(self, num):
        type_of_input = type(num)
        if type_of_input is int:
            self.content.pop(num)
        elif type_of_input is list:
            num = list(set(num))
            num.sort(key=int, reverse=True)
            for index in num:
                self.content.pop(index)

    def get_column(self, column_name):
        column = []
        value_index = self.header.index(column_name)
        for x in self.content:
            column.append(x[value_index])

        return column

    def to_csv(self, path):
        df = self.to_pandas()
        df.to_csv(path)

    def to_pandas(self):
        df = pd.DataFrame(self.content, columns=self.header)
        return df

    def to_dict(self):
        dict_list = []
        length = len(self.content)
        for index in range(0, length):
            row = self.__tuple_to_dict(self.header, self.content[index])
            dict_list.append(row)

        return dict_list

    def __tuple_to_dict(self, header, content):
        row = {}
        length = len(header)
        for index in range(0, length):
            row[header[index]] = content[index]
        return row
