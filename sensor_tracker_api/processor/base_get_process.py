from sensor_tracker_api.builder.simply_meta_data_factory import SimplyMetaDataFactory
from sensor_tracker_api.binder.get_binder import APIGetMethod
from sensor_tracker_api.config.config import Config
from sensor_tracker_api.parser.json_parser import Parser


class BaseGetProcess(object):
    def __init__(self, host):
        self.host = host
        self.APIGetter = APIGetMethod(host=self.host)

        self.format = Config.FORMAT
        self.object_factory = SimplyMetaDataFactory(parser=Parser())

    def get_output_sensors(self, instrument_identifier, instrument_id):
        json_output_sensors = self.APIGetter.get_output_sensors(instrument_identifier=instrument_identifier,
                                                                instrument_id=instrument_id)
        o = self.object_factory.generate_obj(
            **self.__create_input(pattern=self.format["sensor_format"], content=json_output_sensors))
        return o

    def get_sensors(self, instrument_id=None):
        json_sensor = self.APIGetter.get_sensors(instrument_id=instrument_id)
        o = self.object_factory.generate_obj(
            **self.__create_input(pattern=self.format["sensor_format"], content=json_sensor))
        return o

    def get_all_sensors(self):
        return self.get_sensors(None)

    def get_instruments_by_instrument_identifier(self, instrument_identifier):
        json_instrument = self.APIGetter.get_instruments(instrument_identifier=instrument_identifier)
        o = self.object_factory.generate_obj(
            **self.__create_input(pattern=self.format["instrument_format"], content=json_instrument))
        return o

    def get_instruments_by_instrument_id(self, instrument_id):
        json_instrument = self.APIGetter.get_instruments(instrument_id=instrument_id)
        o = self.object_factory.generate_obj(
            **self.__create_input(pattern=self.format["instrument_format"], content=json_instrument))
        return o

    def get_deployment_instruments(self, platform_name, start_time):
        json_deployment_instruments = self.APIGetter.get_deployment_instruments(platform_name=platform_name,
                                                                                start_time=start_time)
        o = self.object_factory.generate_obj(**self.__create_input(pattern=self.format["platform_instrument_format"],
                                                                   content=json_deployment_instruments))
        return o

    def get_all_instruments(self):
        json_instruments = self.APIGetter.get_instruments()

        o = self.object_factory.generate_obj(
            **self.__create_input(pattern=self.format["instrument_format"], content=json_instruments))

        return o

    def get_platform_type(self, model, name):
        json_platform_type = self.APIGetter.get_platform_type(model=model, name=name)
        o = self.object_factory.generate_obj(
            **self.__create_input(pattern=self.format["platform_type_format"], content=json_platform_type))

        return o

    def get_all_platform_type(self):
        return self.get_platform_type(None, None)

    def get_deployments_by_platform_name(self, platform_name):
        json_deployments = self.APIGetter.get_platform_deployments(platform_name=platform_name)
        o = self.object_factory.generate_obj(
            **self.__create_input(pattern=self.format["deployment_format"], content=json_deployments))

        return o

    def get_deployment_by_deployment_number(self, number):
        json_deployments = self.APIGetter.get_platform_deployments(deployment_number=number)
        o = self.object_factory.generate_obj(
            **self.__create_input(pattern=self.format["deployment_format"], content=json_deployments))

        return o

    def get_deployment_by_name_time(self, platform_name, start_time):
        json_platform_deployment = self.APIGetter.get_platform_deployments(platform_name=platform_name,
                                                                           start_time=start_time)
        o = self.object_factory.generate_obj(
            **self.__create_input(pattern=self.format["deployment_format"], content=json_platform_deployment))

        return o

    def get_platform_by_model(self, type):
        platform_json = self.APIGetter.get_platform(platform_type=type)
        o = self.object_factory.generate_obj(
            **self.__create_input(pattern=self.format["platform_format"], content=platform_json))

        return o

    def get_manufacturer_by_manufacturer_id(self, manufacturer_id):
        json_manufacturer = self.APIGetter.get_manufacturer(manufacturer_id=manufacturer_id)

    def get_instruments_on_platform_by_name(self, platform_name):
        instruments_obj = self.APIGetter.get_instruments_on_platform(platform_name=platform_name)
        o = self.object_factory.generate_obj(
            **self.__create_input(pattern=self.format["instrument_all_format"], content=instruments_obj))

        return o

    def get_platform_deployment_comments(self, platform_name, start_time):
        comments_obj = self.APIGetter.get_platform_deployment_comments(platform_name=platform_name,
                                                                       start_time=start_time)
        o = self.object_factory.generate_obj(
            **self.__create_input(pattern=self.format["deployment_comment_format"], content=comments_obj))
        return o

    def __create_input(self, pattern=None, content=None):
        res = dict(
            pattern=pattern,
            content=content
        )
        return res

    def get_platform_id(self, platform_name):
        res = None
        platform_json = self.APIGetter.get_platform(platform_name=platform_name)
        if platform_json:
            res = self.__fetch_id(platform_json[0])
        return res

    def get_power_id(self, power_name):
        res = None
        power_json = self.APIGetter.get_power(power_name=power_name)
        if power_json:
            res = self.__fetch_id(power_json[0])
        return res

    def get_project_id(self, project_name):
        res = None
        project_json = self.APIGetter.get_project(project_name=project_name)
        if project_json:
            res = self.__fetch_id(project_json[0])
        return res

    def get_institution_id(self, institution_name):
        res = None
        institution_json = self.APIGetter.get_institution(institution_name=institution_name)
        if institution_json:
            res = self.__fetch_id(institution_json[0])
        return res

    def __fetch_id(self, j, id_name=None):
        id = "id"
        if id_name:
            id = id_name
        res = j[id]
        return res


p = BaseGetProcess("http://127.0.0.1:8001/api/")
n = p.get_institution_id("Dalhousie, Oceaanography")
print(n)
# print(p.get_output_sensors_by_platform("dal556", "2017-06-05 15:13:26"))
# ob = p.get_deployments_by_general_model("slocum")
# print(ob.to_dict())
# print(p.get_instruments_on_platform_by_name("dal556").to_csv("/Users/xiang/Desktop/output/5.csv"))
