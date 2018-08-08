import os, glob
import pandas as pd


class CsvReader(object):
    """
    The object can take path, if the path is a csv file, then it create a single dataframe,
    if path it is a directory, it will search all csv files that under the directory path and
    create a dict with panda data frames, which keys is the file name and the value is panda data
    frame.
    """

    def __init__(self, path):
        self.file_name = []
        self.df_list = []
        if os.path.isfile(path):
            self.__read_csv_file(path)
        elif os.path.isdir(path):
            num = self.__read_csvs_from_dir(path)
            print("directory path is valid, %d csv file is found" % num)
        else:
            raise Warning("invalid path")

    def get_df(self):
        res = None
        if self.df_list is not []:
            res = self.df_list
        return res

    def get_df_list(self, with_names=None):
        if with_names is None:
            res = self.get_df_list()
        else:
            res = []
            for x in self.df_list:
                res.append(x)
        return res

    def get_dfs_in_dict(self):
        res = []
        for index in self.file_name:
            name = self.file_name[index]
            value = self.df_list[index]
            res.append({name: value})
        return res


    def __read_csv_file(self, path):
        try:
            df = pd.read_csv(path)
        except Exception as e:
            print(e)
            df = weird_csv(path)
        file_name = os.path.basename(path)
        name = os.path.splitext(file_name)[0]

        self.file_name.append(name)
        self.df_list.append(df)

    def __read_csvs_from_dir(self, path):
        os.chdir(path)
        for f in glob.glob("*.csv"):
            self.__read_csv_file(f)

        return len(glob.glob("*.csv"))

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
