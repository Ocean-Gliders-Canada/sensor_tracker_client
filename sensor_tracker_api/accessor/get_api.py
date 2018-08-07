from sensor_tracker_api.accessor.api import AccessApi


class GetApi(AccessApi):
    def __init__(self, **kwargs):
        AccessApi.__init__(self, **kwargs)

    def get_deployments(self, *args, **kwargs):
        """
        Input cloud be deployment number, or platform type or, platform name or platform name and start time

        :param specific:
        :param para:
        :return: relevant deployments data in pandas format
        """
        checker = self.arg_check.deployment_input_check
        arg_type = self.__input_check(checker, *args, **kwargs)

        res = None

        if arg_type == self.config.ARG_TYPE["INVALID"]:
            raise TypeError("Invalid Input")
        elif arg_type == self.config.ARG_TYPE["general_model"]:
            res = self.process.get_deployments_by_general_model(*args)
        elif arg_type == self.config.ARG_TYPE["deployment_number"]:
            res = self.process.get_deployment_by_deployment_number(*args)
        elif arg_type == self.config.ARG_TYPE["model"]:
            res = self.process.get_deployment_by_model(*args)
        elif arg_type == self.config.ARG_TYPE["platform_name"]:
            res = self.process.get_deployments_by_platform_name(*args)
        elif arg_type == self.config.ARG_TYPE["name_time"]:
            res = self.process.get_deployment_by_name_time(*args)

        return res

    def get_sensors(self, *args, **kwargs):
        output = kwargs.pop("output", True)
        checker = self.arg_check.sensor_input_check
        arg_type = self.__input_check(checker, *args, **kwargs)
        res = None
        if arg_type == self.config.ARG_TYPE["INVALID"]:
            raise TypeError("Invalid Input")
        elif arg_type == self.config.ARG_TYPE["name_time"]:
            if output:
                res = self.process.get_output_sensors_by_deployment(*args)
            else:
                res = self.process.get_sensors_on_deployment(*args)
        return res

    def get_instruments(self, *args, **kwargs):
        checker = self.arg_check.instrument_input_check
        arg_type = self.__input_check(checker, *args, **kwargs)

        res = None
        if arg_type == self.config.ARG_TYPE["INVALID"]:
            raise TypeError("Invalid Input")
        elif arg_type == self.config.ARG_TYPE["deployment_number"]:
            platform_name, start_time = self.get_deployment_info(*args)
            res = self.process.get_instrument_on_deployment(platform_name, start_time)
        elif arg_type == self.config.ARG_TYPE["platform_name"]:
            res = self.process.get_instruments_on_platform_by_name(*args)
        elif arg_type == self.config.ARG_TYPE["name_time"]:
            res = self.process.get_instrument_on_deployment(*args)

        return res

    def get_deployment_comments(self, *args, **kwargs):
        checker = self.arg_check.deployment_comment_input_check
        arg_type = self.__input_check(checker, *args, **kwargs)
        res = None

        if arg_type == self.config.ARG_TYPE["INVALID"]:
            raise TypeError("Invalid Input")
        elif arg_type == self.config.ARG_TYPE["deployment_number"]:
            platform_name, start_time = self.get_deployment_info(*args)
            res = self.process.get_platform_deployment_comments(platform_name, start_time)
        elif arg_type == self.config.ARG_TYPE["name_time"]:
            res = self.process.get_platform_deployment_comments(*args)

        return res

    def get_platform(self, *args, **kwargs):

        checker = self.arg_check.deployment_input_check
        arg_type = self.__input_check(checker, *args, **kwargs)

        res = None

        if arg_type == self.config.ARG_TYPE["INVALID"]:
            raise TypeError("Invalid Input")
        elif arg_type == self.config.ARG_TYPE["general_model"]:
            res = self.process.get_platform_by_general_model(*args)
        elif arg_type == self.config.ARG_TYPE["model"]:
            res = self.process.get_platform_by_model(*args)

        return res

    def __input_check(self, checker, *args, **kwargs):
        arg_type = kwargs.pop("arg_type", None)
        if arg_type in self.config.ARG_TYPE:
            arg_type = self.config.ARG_TYPE[arg_type]
        else:
            arg_type = None
        if not arg_type:
            arg_type = checker(*args, **kwargs)

        return arg_type

    def get_deployment_info(self, deployment_num):
        obj = self.process.get_deployment_by_deployment_number(deployment_num)
        data_dict = obj.to_dict()[0]
        platform_name = data_dict["platform_name"]
        start_time = data_dict['start_time']
        return platform_name, start_time

    def is_testing_mission(self, platform_name, start_time):
        obj = self.get_deployments(platform_name, start_time)
        res = obj.get_column("testing_mission")
        testing = res[0]
        if not testing:
            testing = False
        return testing

    def get_mission_id(self, platform_name, start_time):
        obj = self.get_deployments(platform_name, start_time)
        res = obj.get_column("deployment_number")
        num = res[0]
        return num
