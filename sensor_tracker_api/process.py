from sensor_tracker_api.simply_meta_data_factory import SimplyMetaDataFactory
from sensor_tracker_api.binder import APIGetMethod
from sensor_tracker_api.config import Config
from sensor_tracker_api.parser import Parser


class Process(object):
    def __init__(self, host):
        self.host = host
        self.APIGetter = APIGetMethod(host=self.host)
        self.parsers = Parser()
        self.format = Config.FORMAT
        self.object_factory = SimplyMetaDataFactory()

    def get_sensors_on_deployment(self, platform_name, start_time):
        instrument = self.get_deployment_instruments(platform_name, start_time)

        instrument_ids = instrument.get_column('instrument__id')

        sensor_obj = None
        for ID in instrument_ids:
            sensor = self.get_sensors(ID)
            if sensor_obj:
                sensor_obj.add(sensor)
            else:
                sensor_obj = sensor

        return sensor_obj

    def get_output_sensors_by_deployment(self, platform_name, start_time):
        instrument = self.get_deployment_instruments(platform_name, start_time)

        instrument_ids = instrument.get_column('instrument__id')

        sensor_obj = None
        for ID in instrument_ids:
            sensor = self.get_output_sensors(None, ID)
            if sensor_obj:
                sensor_obj.add(sensor)
            else:
                sensor_obj = sensor

        return sensor_obj

    def get_output_sensors(self, instrument_identifier, instrument_id):
        json_output_sensors = self.APIGetter.get_output_sensors(instrument_identifier=instrument_identifier,
                                                                instrument_id=instrument_id)
        header, rows = self.parsers.parse(self.format["sensor_format"], json_output_sensors)
        o = self.object_factory.create(header=header, content=rows)
        return o

    def get_sensors(self, instrument_id=None):
        json_sensor = self.APIGetter.get_sensors(instrument_id=instrument_id)
        header, rows = self.parsers.parse(self.format["sensor_format"], json_sensor)
        o = self.object_factory.create(header=header, content=rows)
        return o

    def get_all_sensors(self):
        return self.get_sensors(None)

    def get_instruments_by_instrument_identifier(self, instrument_identifier):
        json_instrument = self.APIGetter.get_instruments(instrument_identifier=instrument_identifier)
        header, rows = self.parsers.parse(self.format["instrument_format"], json_instrument)
        o = self.object_factory.create(header=header, content=rows)
        return o

    def get_instruments_by_instrument_id(self, instrument_id):
        json_instrument = self.APIGetter.get_instruments(instrument_id=instrument_id)
        header, rows = self.parsers.parse(self.format["instrument_format"], json_instrument)
        o = self.object_factory.create(header=header, content=rows)
        return o

    def get_deployment_instruments(self, platform_name, start_time):
        json_deployment_instruments = self.APIGetter.get_deployment_instruments(platform_name=platform_name,
                                                                                start_time=start_time)
        header, rows = self.parsers.parse(self.format["platform_instrument_format"], json_deployment_instruments)
        o = self.object_factory.create(header=header, content=rows)
        return o

    def get_instrument_on_deployment(self, platform_name, start_time):
        deployment_instruments_obj = self.get_deployment_instruments(platform_name, start_time)
        instruments_ids = deployment_instruments_obj.get_column("instrument__id")
        instrument_obj = None
        for ID in instruments_ids:
            instrument_df = self.get_instruments_by_instrument_id(ID)
            if instrument_obj:
                instrument_obj.add(instrument_df)
            else:
                instrument_obj = instrument_df

        return instrument_obj

    def get_all_instruments(self):
        json_instruments = self.APIGetter.get_instruments()
        header, rows = self.parsers.parse(self.format["instrument_format"], json_instruments)
        o = self.object_factory.create(header=header, content=rows)
        return o

    def get_platform_type(self, model, name):
        json_platform_type = self.APIGetter.get_platform_type(model=model, name=name)
        header, rows = self.parsers.parse(self.format["platform_type_format"], json_platform_type)
        o = self.object_factory.create(header=header, content=rows)
        return o

    def get_platform_type_by_general_model(self, general_model):
        platform_model_obj = self.get_all_platform_type()
        general_model = general_model.lower()
        models = platform_model_obj.get_column("model")
        length = len(models)
        model_remove = []
        for index in range(0, length):
            model = models[index]
            if general_model not in model.lower():
                model_remove.append(index)

        platform_model_obj.remove(model_remove)
        return platform_model_obj

    def get_all_platform_type(self):
        return self.get_platform_type(None, None)

    def get_deployments_by_general_model(self, general_model):
        platform_obj = self.get_platform_by_model(general_model)
        platform_names = platform_obj.get_column("name")
        deployment_objs = None
        for name in platform_names:
            deployment_obj = self.get_deployments_by_platform_name(name)
            if deployment_objs:
                deployment_objs.add(deployment_obj)
            else:
                deployment_objs = deployment_obj
        return deployment_objs

    def get_deployment_by_model(self, model):
        platform_obj = self.get_platform_by_type(model)
        platform_names = platform_obj.get_column("name")
        deployment_objs = None
        for name in platform_names:
            deployment_obj = self.get_deployments_by_platform_name(name)
            if deployment_objs:
                deployment_objs.add(deployment_obj)
            else:
                deployment_objs = deployment_obj
        return deployment_objs

    def get_deployments_by_platform_name(self, platform_name):
        json_deployments = self.APIGetter.get_platform_deployments(platform_name=platform_name)
        header, rows = self.parsers.parse(self.format["deployment_format"], json_deployments)
        o = self.object_factory.create(header=header, content=rows)
        return o

    def get_deployment_by_deployment_number(self, number):
        json_deployments = self.APIGetter.get_platform_deployments(deployment_number=number)
        header, rows = self.parsers.parse(self.format["deployment_format"], json_deployments)
        o = self.object_factory.create(header=header, content=rows)
        return o

    def get_deployment_by_name_time(self, platform_name, start_time):
        json_platform_deployment = self.APIGetter.get_platform_deployments(platform_name=platform_name,
                                                                           start_time=start_time)
        header, rows = self.parsers.parse(self.format["deployment_format"], json_platform_deployment)
        o = self.object_factory.create(header=header, content=rows)
        return o

    def get_platform_by_type(self, type):
        platform_json = self.APIGetter.get_platform(platform_type=type)
        header, rows = self.parsers.parse(self.format["platform_format"], platform_json)
        o = self.object_factory.create(header=header, content=rows)
        return o

    def get_platform_by_model(self, model):
        platform_model_obj = self.get_platform_type_by_general_model(model)
        models = platform_model_obj.get_column("model")
        platform_obj = None
        for model in models:
            if not platform_obj:
                platform_obj = self.get_platform_by_type(model)
            else:
                platform_obj.add(self.get_platform_by_type(model))

        return platform_obj

    def get_manufacturer_by_manufacturer_id(self, manufacturer_id):
        json_manufacturer = self.APIGetter.get_manufacturer(manufacturer_id=manufacturer_id)

    def get_instruments_on_platform_by_name(self, platform_name):
        instruments_obj = self.APIGetter.get_instruments_on_platform(platform_name=platform_name)
        header, rows = self.parsers.parse(self.format["instrument_all_format"], instruments_obj)
        o = self.object_factory.create(header=header, content=rows)
        return o

    def get_platform_deployment_comments(self, platform_name, start_time):
        comments_obj = self.APIGetter.get_platform_deployment_comments(platform_name=platform_name,
                                                                       start_time=start_time)
        header, rows = self.parsers.parse(self.format["deployment_comment_format"], comments_obj)
        o = self.object_factory.create(header=header, content=rows)
        return o

# p = Process("http://127.0.0.1:8000/api/")
# print(p.get_output_sensors_by_platform("dal556", "2017-06-05 15:13:26"))
# ob = p.get_deployments_by_general_model("slocum")
# print(ob.to_dict())
# print(p.get_instruments_on_platform_by_name("dal556").to_csv("/Users/xiang/Desktop/output/5.csv"))
