from sensor_tracker_api.processor.base_get_process import BaseGetProcess


class Process(BaseGetProcess):
    def __init__(self, host):
        BaseGetProcess.__init__(self, host)

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

    def get_deployments_by_general_model(self, general_model):
        platform_obj = self.get_platform_by_general_model(general_model)
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
        platform_obj = self.get_platform_by_model(model)
        platform_names = platform_obj.get_column("name")
        deployment_objs = None
        for name in platform_names:
            deployment_obj = self.get_deployments_by_platform_name(name)
            if deployment_objs:
                deployment_objs.add(deployment_obj)
            else:
                deployment_objs = deployment_obj
        return deployment_objs

    def get_platform_by_general_model(self, model):
        platform_model_obj = self.get_platform_type_by_general_model(model)
        models = platform_model_obj.get_column("model")
        platform_obj = None
        for model in models:
            if not platform_obj:
                platform_obj = self.get_platform_by_model(model)
            else:
                platform_obj.add(self.get_platform_by_model(model))

        return platform_obj

# p = Process("http://127.0.0.1:8000/api/")
# print(p.get_output_sensors_by_platform("dal556", "2017-06-05 15:13:26"))
# ob = p.get_deployments_by_general_model("slocum")
# print(ob.to_dict())
# print(p.get_instruments_on_platform_by_name("dal556").to_csv("/Users/xiang/Desktop/output/5.csv"))
