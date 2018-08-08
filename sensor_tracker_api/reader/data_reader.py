from sensor_tracker_api.builder.simply_meta_data_factory import SimplyMetaDataFactory
from sensor_tracker_api.reader.csv_reader import CsvReader
from sensor_tracker_api.parser.pd_parser import Parser


class DataReader(CsvReader):
    def __init__(self, path):
        CsvReader.__init__(self, path)
        self.factory = SimplyMetaDataFactory(parser=Parser())

    def generate_obj(self):
        df = self.get_df()
        param = {"df" : df}
        obj = self.factory.generate_obj(**param)
        return obj


o = DataReader("/Users/xiang/Desktop/output/sample.csv")
res = o.generate_obj()

print(res)
