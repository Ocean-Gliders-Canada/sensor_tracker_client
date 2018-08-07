from sensor_tracker_api.binder.binder import APIMethod


class APIGetMethod(APIMethod):
    def __init__(self, **kwargs):
        APIMethod.__init__(self, **kwargs)

    def get_platform_deployments(self, **kwargs):
        platform_name = kwargs.pop("platform_name", None)
        start_time = kwargs.pop("start_time", None)
        deployment_number = kwargs.pop("deployment_number", None)
        if platform_name and start_time:
            result = self.parse_content("get_platform_deployments", {"name": platform_name, "time": start_time})
        elif platform_name:
            result = self.parse_content("get_platform_deployments", {"name": platform_name})
        elif deployment_number:
            result = self.parse_content("get_platform_deployments", {"deployment_number": str(deployment_number)})
        else:
            result = self.parse_content("get_platform_deployments")

        return result

    def get_instruments(self, **kwargs):
        instrument_identifier = kwargs.pop("instrument_identifier", None)
        instrument_id = kwargs.pop("instrument_id", None)
        instrument_serial = kwargs.pop("serial", None)
        param = {}
        if instrument_id:
            param["id"] = instrument_id
            result = self.parse_content("get_instruments", param)
        elif instrument_identifier or instrument_serial:
            param = {}
            if instrument_identifier:
                param["identifier"] = instrument_identifier
            if instrument_serial:
                param["serial"] = instrument_serial
            result = self.parse_content("get_instruments", param)
        else:
            result = self.parse_content("get_instruments")
        return result

    def get_deployment_instruments(self, **kwargs):
        platform_name = kwargs.pop("platform_name", None)
        start_time = kwargs.pop("start_time", None)

        result = self.parse_content("get_deployment_instruments", {"name": platform_name, "time": start_time})
        return result

    def get_instruments_on_platform(self, **kwargs):
        platform_name = kwargs.pop("platform_name", None)
        result = self.parse_content("get_instruments_on_platform", {"name": platform_name})
        return result

    def get_sensors(self, **kwargs):
        instrument_id = kwargs.pop("instrument_id", None)
        if instrument_id:
            result = self.parse_content("get_sensors", {"instrument_id": instrument_id})
        else:
            result = self.parse_content("get_sensors")
        return result

    def get_output_sensors(self, **kwargs):
        """
        Get output sensor
        :param kwargs:
        :return:
        """
        instrument_identifier = kwargs.pop("instrument_identifier", None)
        instrument_id = kwargs.pop("instrument_id", None)
        para = {}
        if instrument_identifier:
            para["identifier"] = instrument_identifier
        elif instrument_id:
            para["id"] = instrument_id

        result = self.parse_content("get_output_sensors", para)

        return result

    def get_platform_deployment_comments(self, **kwargs):
        name = kwargs.pop("platform_name", None)
        time = kwargs.pop("start_time", None)
        para = {"name": name, "time": time}
        result = self.parse_content("get_platform_deployment_comments", para)

        return result

    def get_platform_type(self, **kwargs):
        model = kwargs.pop("model", None)
        name = kwargs.pop("name", None)
        para = {}
        if model:
            para["model"] = model
        elif name:
            para["name"] = name

        result = self.parse_content("get_platform_type", para)
        return result

    def get_platform(self, **kwargs):
        platform_id = kwargs.pop("platform_id", None)
        platform_name = kwargs.pop("platform_name", None)
        platform_type = kwargs.pop("platform_type", None)

        para = {}
        if platform_type:
            para["type"] = platform_type
        if platform_name:
            para["name"] = platform_name
        elif platform_id:
            para["id"] = platform_id

        result = self.parse_content("get_platform", para)

        return result

    def get_manufacturer(self, **kwargs):
        manufacturer_id = kwargs.pop("manufacturer_id", None)
        manufacturer_name = kwargs.pop("manufacturer_name", None)
        para = {}
        if manufacturer_id:
            para["id"] = manufacturer_id
        elif manufacturer_name:
            para["name"] = manufacturer_name

        result = self.parse_content("get_platform", para)

        return result

# p = APIGetMethod(host="http://127.0.0.1:8000/api/")
# print(p.get_output_sensors_by_platform("dal556", "2017-06-05 15:13:26"))
# ob = p.get_deployments_by_general_model("slocum")
# print(ob.to_dict())
# print(p.get_platform_deployment_comments(platform_name="dal556", start_time="2017-06-05 15:13:26"))
