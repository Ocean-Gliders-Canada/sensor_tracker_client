import pandas as pd

from sensor_tracker_api.binder import APIGetMethod
from sensor_tracker_api.parsers import Parser
from sensor_tracker_api.config import Config


class Process(object):
    def __init__(self, host):
        self.host = host
        self.APIGetter = APIGetMethod(host=self.host)
        self.parsers = Parser()
        self.format = Config.FORMAT

    def get_sensors_on_deployment(self, platform_name, start_time):
        instrument = self.get_deployment_instruments(platform_name, start_time)

        instrument_ids = instrument['instrument__id'].tolist()

        sensor_dfs = []
        for ID in instrument_ids:
            sensor = self.get_sensors(ID)
            sensor_dfs.append(sensor)

        df = pd.concat(sensor_dfs, ignore_index=True)

        return df

    def get_output_sensors_by_deployment(self, platform_name, start_time):
        instrument = self.get_deployment_instruments(platform_name, start_time)

        instrument_ids = instrument['instrument__id'].tolist()

        sensor_dfs = []
        for ID in instrument_ids:
            sensor = self.get_output_sensors(None, ID)
            sensor_dfs.append(sensor)

        df = pd.concat(sensor_dfs, ignore_index=True)
        return df

    def get_output_sensors(self, instrument_identifier, instrument_id):
        json_output_sensors = self.APIGetter.get_output_sensors(instrument_identifier=instrument_identifier,
                                                                instrument_id=instrument_id)
        header, rows = self.parsers.parse(self.format["sensor_format"], json_output_sensors)
        df = pd.DataFrame(rows, columns=header)
        return df

    def get_sensors(self, instrument_id=None):
        json_sensor = self.APIGetter.get_sensors(instrument_id=instrument_id)
        header, rows = self.parsers.parse(self.format["sensor_format"], json_sensor)
        df = pd.DataFrame(rows, columns=header)
        return df

    def get_all_sensors(self):
        return self.get_sensors(None)

    def get_instruments_by_instrument_identifier(self, instrument_identifier):
        json_instrument = self.APIGetter.get_instruments(instrument_identifier=instrument_identifier)
        header, rows = self.parsers.parse(self.format["instrument_format"], json_instrument)
        df = pd.DataFrame(rows, columns=header)
        return df

    def get_instruments_by_instrument_id(self, instrument_id):
        json_instrument = self.APIGetter.get_instruments(instrument_id=instrument_id)
        header, rows = self.parsers.parse(self.format["instrument_format"], json_instrument)
        df = pd.DataFrame(rows, columns=header)
        return df

    def get_deployment_instruments(self, platform_name, start_time):
        json_deployment_instruments = self.APIGetter.get_deployment_instruments(platform_name=platform_name,
                                                                                start_time=start_time)
        header, rows = self.parsers.parse(self.format["platform_instrument_format"], json_deployment_instruments)
        df = pd.DataFrame(rows, columns=header)
        return df

    def get_instrument_on_deployment(self, platform_name, start_time):
        deployment_instruments_df = self.get_deployment_instruments(platform_name, start_time)
        instruments_ids = deployment_instruments_df["instrument__id"].tolist()
        instrument_dfs = []
        for ID in instruments_ids:
            instrument_df = self.get_instruments_by_instrument_id(ID)
            instrument_dfs.append(instrument_df)

        df = pd.concat(instrument_dfs, ignore_index=True)
        return df

    def get_all_instruments(self):
        json_instruments = self.APIGetter.get_instruments()
        header, rows = self.parsers.parse(self.format["instrument_format"], json_instruments)
        df = pd.DataFrame(rows, columns=header)
        return df

    def get_platform_type(self, model, name):
        json_platform_type = self.APIGetter.get_platform_type(model=model, name=name)
        header, rows = self.parsers.parse(self.format["platform_type_format"], json_platform_type)
        df = pd.DataFrame(rows, columns=header)
        return df

    def get_platform_type_by_general_model(self, general_model):
        platform_model_df = self.get_all_platform_type()
        general_model = general_model.lower()
        models = platform_model_df["model"].tolist()
        length = len(models)
        model_remove = []
        for index in range(0, length):
            model = models[index]
            if general_model not in model.lower():
                model_remove.append(index)

        df = platform_model_df.drop(model_remove)
        return df

    def get_all_platform_type(self):
        return self.get_platform_type(None, None)

    def get_deployments_by_general_model(self, general_model):
        platform_df = self.get_platform_by_model(general_model)
        platform_names = platform_df["name"].tolist()
        deployment_dfs = []
        for name in platform_names:
            deployment_df = self.get_deployments_by_platform_name(name)
            deployment_dfs.append(deployment_df)
        df = pd.concat(deployment_dfs, ignore_index=True)
        return df

    def get_deployments_by_platform_name(self, platform_name):
        json_deployments = self.APIGetter.get_platform_deployments(platform_name=platform_name)
        header, rows = self.parsers.parse(self.format["deployment_format"], json_deployments)
        df = pd.DataFrame(rows, columns=header)
        return df

    def get_deployment_by_deployment_number(self, number):
        json_deployments = self.APIGetter.get_platform_deployments(deployment_number=number)
        header, rows = self.parsers.parse(self.format["deployment_format"], json_deployments)
        df = pd.DataFrame(rows, columns=header)
        return df

    def get_deployment_by_name_time(self, platform_name, start_time):
        json_platform_deployment = self.APIGetter.get_platform_deployments(platform_name=platform_name,
                                                                           start_time=start_time)
        header, rows = self.parsers.parse(self.format["deployment_format"], json_platform_deployment)
        df = pd.DataFrame(rows, columns=header)
        return df

    def get_platform_by_type(self, type):
        platform_json = self.APIGetter.get_platform(platform_type=type)
        header, rows = self.parsers.parse(self.format["platform_format"], platform_json)
        df = pd.DataFrame(rows, columns=header)
        return df

    def get_platform_by_model(self, model):
        platform_model_df = self.get_platform_type_by_general_model(model)
        models = platform_model_df["model"].tolist()
        platform_dfs = []
        for model in models:
            platform_df = self.get_platform_by_type(model)
            platform_dfs.append(platform_df)

        df = pd.concat(platform_dfs, ignore_index=True)

        return df

    def get_manufacturer_by_manufacturer_id(self, manufacturer_id):
        json_manufacturer = self.APIGetter.get_manufacturer(manufacturer_id=manufacturer_id)



p = Process("http://127.0.0.1:8000/api/")
# print(p.get_output_sensors_by_platform("dal556", "2017-06-05 15:13:26"))
df1 = p.get_deployments_by_general_model("Slocum")
print(df1.to_dict('records'))
# print(p.get_all_sensors())
