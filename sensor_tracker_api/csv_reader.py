import os, glob
import pandas as pd


class CsvReader(object):
    def __init__(self, path):

        self.data = {}
        if os.path.isfile(path):
            self.read_csv_file(path)
            print("path is valid")
        elif os.path.isdir(path):
            num = self.get_csv_dir(path)
            print("directory path is valid, %d csv file is found" % num)
        else:
            print("invalid path")
            exit(1)

        self.remove_null_rows()

    def read_csv_file(self, path):

        try:
            df = pd.read_csv(path)
        except pd.errors.ParserError as e:
            df = weird_csv(path)
        file_name = os.path.basename(path)
        name = os.path.splitext(file_name)[0]

        self.data[name] = df

    def get_csv_dir(self, path):
        try:
            os.path.isfile(path)
        except ValueError:
            raise Exception('file path is invaild')
        os.chdir(path)
        for f in glob.glob("*.csv"):
            self.read_csv_file(f)

        return len(glob.glob("*.csv"))

    def remove_null_rows(self):

        for df in self.data:
            self.data[df] = self.data[df].dropna(how="all")
            self.data[df] = self.data[df].reset_index(drop=True)


def weird_csv(path):
    with open(path) as f:
        content = f.readlines()
    content = [x.strip() for x in content]

    labels = content.pop(0)


    l = labels.split(',')
    labels_length = len(l)

    def split_into_list(s, le):
        result = ()
        for x in range(0, (le - 1)):
            index = s.find(',')
            result = result + ((s[:index]),)
            s = s[index:]
            if s[0] == ',':
                s = s[1:]
        result = result + (s,)
        return result

    c = []
    for x in content:
        c.append(split_into_list(x, labels_length))

    df = pd.DataFrame.from_records(c, columns=l)

    return df
