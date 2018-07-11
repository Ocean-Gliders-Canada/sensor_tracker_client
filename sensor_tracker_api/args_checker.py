import time


class InputChecker(object):
    def __init__(self, config):
        self.config = config

    def deployment_input_check(self, *args, **kwargs):
        length_of_input = len(args)
        if length_of_input == 1:
            value = args[0]
            t = type(value)
            if t is int:
                return self.config.ARG_TYPE["deployment_number"]
            elif t is str:
                is_int = value.isdigit()
                if is_int:
                    return self.config.ARG_TYPE["deployment_number"]
                else:
                    value = value.lower()
                    if value in self.config.GLIDER_TYPE:
                        return self.config.ARG_TYPE["general_model"]
                    elif list_value_in_value(self.config.GLIDER_TYPE, value):
                        return self.config.ARG_TYPE["model"]
                    else:
                        return self.config.ARG_TYPE["platform_name"]
        elif length_of_input == 2:
            value1 = args[0]
            value2 = args[1]
            try:
                time.strptime(value2, '%Y-%m-%d %H:%M:%S')
                if type(value1) is str:
                    return self.config.ARG_TYPE["name_time"]
            except ValueError:
                pass

        return self.config.ARG_TYPE["INVALID"]

    def sensor_input_check(self, *args, **kwargs):
        output = kwargs.pop("output", True)
        length_of_input = len(args)
        if length_of_input == 1:
            value = args[0]
            t = type(value)
            if t is int:
                return self.config.ARG_TYPE["deployment_number"]
            elif t is str:
                is_int = value.isdigit()
                if is_int:
                    return self.config.ARG_TYPE["deployment_number"]
                else:
                    value = value.lower()
                    if value in self.config.GLIDER_TYPE:
                        return self.config.ARG_TYPE["general_model"]
                    elif list_value_in_value(self.config.GLIDER_TYPE, value):
                        return self.config.ARG_TYPE["model"]
                    else:
                        return self.config.ARG_TYPE["platform_name"]
        elif length_of_input == 2:
            value1 = args[0]
            value2 = args[1]
            try:
                time.strptime(value2, '%Y-%m-%d %H:%M:%S')
                if type(value1) is str:
                    return self.config.ARG_TYPE["name_time"]
            except ValueError:
                pass

        return self.config.ARG_TYPE["INVALID"]

    def instrument_input_check(self, *args, **kwargs):
        length_of_input = len(args)
        if length_of_input == 1:
            value = args[0]
            t = type(value)
            if t is int:
                return self.config.ARG_TYPE["deployment_number"]
            elif t is str:
                is_int = value.isdigit()
                if is_int:
                    return self.config.ARG_TYPE["deployment_number"]
                else:
                    return self.config.ARG_TYPE["platform_name"]
        elif length_of_input == 2:
            return self.config.ARG_TYPE["name_time"]

        return self.config.ARG_TYPE["INVALID"]

    def deployment_comment_input_check(self, *args, **kwargs):
        length_of_input = len(args)
        if length_of_input == 1:
            value = args[0]
            t = type(value)
            if t is int:
                return self.config.ARG_TYPE["deployment_number"]
            elif t is str:
                is_int = value.isdigit()
                if is_int:
                    return self.config.ARG_TYPE["deployment_number"]
        elif length_of_input == 2:
            return self.config.ARG_TYPE["name_time"]

        return self.config.ARG_TYPE["INVALID"]

    def platform_input_checker(self, *args, **kwargs):
        length_of_input = len(args)
        if length_of_input == 1:
            value = args[0]
            t = type(value)
            if t is str:
                value = value.lower()
                if value in self.config.GLIDER_TYPE:
                    return self.config.ARG_TYPE["general_model"]
                elif list_value_in_value(self.config.GLIDER_TYPE, value):
                    return self.config.ARG_TYPE["model"]

        return self.config.ARG_TYPE["INVALID"]


def list_value_in_value(array, value):
    res = False
    for v in array:
        if v in value:
            res = True
            break
    return res
