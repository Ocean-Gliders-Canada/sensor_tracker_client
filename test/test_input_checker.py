import unittest

from sensor_tracker_api.config import Config
from sensor_tracker_api.checker.args_checker import InputChecker


class TestInputChecker(unittest.TestCase):
    def setUp(self):
        self.arg_check = InputChecker(Config)
        self.arg1 = 1
        self.arg2 = "wave"
        self.arg3 = "Slocum Glider G3"
        self.arg4 = ("DL", "2018-04-03 12:00:00")
        self.arg5 = "otn200"
        self.arg6 = "2"
        self.arg7 = ("DL", "2018-04-03")
        self.arg8 = ("DL", "2018-04-03 12")

    def test_deployment_input_check(self):
        self.assertEqual(self.arg_check.deployment_input_check(self.arg1), Config.ARG_TYPE["deployment_number"])
        self.assertEqual(self.arg_check.deployment_input_check(self.arg2), Config.ARG_TYPE["general_model"])
        self.assertEqual(self.arg_check.deployment_input_check(self.arg3), Config.ARG_TYPE["model"])
        self.assertEqual(self.arg_check.deployment_input_check(*self.arg4), Config.ARG_TYPE["name_time"])
        self.assertEqual(self.arg_check.deployment_input_check(self.arg5), Config.ARG_TYPE["platform_name"])
        self.assertEqual(self.arg_check.deployment_input_check(self.arg6), Config.ARG_TYPE["deployment_number"])
        self.assertEqual(self.arg_check.deployment_input_check(*self.arg7), Config.ARG_TYPE["INVALID"])
        self.assertEqual(self.arg_check.deployment_input_check(*self.arg8), Config.ARG_TYPE["INVALID"])

    def test_sensor_input_check(self):
        self.assertEqual(self.arg_check.sensor_input_check(self.arg1), Config.ARG_TYPE["deployment_number"])
        self.assertEqual(self.arg_check.sensor_input_check(self.arg2), Config.ARG_TYPE["general_model"])
        self.assertEqual(self.arg_check.sensor_input_check(self.arg3), Config.ARG_TYPE["model"])
        self.assertEqual(self.arg_check.sensor_input_check(*self.arg4), Config.ARG_TYPE["name_time"])
        self.assertEqual(self.arg_check.sensor_input_check(self.arg5), Config.ARG_TYPE["platform_name"])
        self.assertEqual(self.arg_check.sensor_input_check(self.arg6), Config.ARG_TYPE["deployment_number"])
        self.assertEqual(self.arg_check.sensor_input_check(*self.arg7), Config.ARG_TYPE["INVALID"])
        self.assertEqual(self.arg_check.deployment_input_check(*self.arg8), Config.ARG_TYPE["INVALID"])

    def test_instrument_input_check(self):
        self.assertEqual(self.arg_check.instrument_input_check(self.arg1), Config.ARG_TYPE["deployment_number"])
        self.assertEqual(self.arg_check.instrument_input_check(*self.arg4), Config.ARG_TYPE["name_time"])
        self.assertEqual(self.arg_check.instrument_input_check(self.arg5), Config.ARG_TYPE["platform_name"])
        self.assertEqual(self.arg_check.instrument_input_check(self.arg6), Config.ARG_TYPE["deployment_number"])
        self.assertEqual(self.arg_check.instrument_input_check(*self.arg7), Config.ARG_TYPE["INVALID"])
        self.assertEqual(self.arg_check.deployment_input_check(*self.arg8), Config.ARG_TYPE["INVALID"])

    def test_deployment_comment_input_check(self):
        self.assertEqual(self.arg_check.deployment_comment_input_check(self.arg1), Config.ARG_TYPE["deployment_number"])
        self.assertEqual(self.arg_check.deployment_comment_input_check(*self.arg4), Config.ARG_TYPE["name_time"])
        self.assertEqual(self.arg_check.deployment_comment_input_check(self.arg6), Config.ARG_TYPE["deployment_number"])
        self.assertEqual(self.arg_check.deployment_comment_input_check(*self.arg7), Config.ARG_TYPE["INVALID"])
        self.assertEqual(self.arg_check.deployment_input_check(*self.arg8), Config.ARG_TYPE["INVALID"])

    def test_platform_input_checker(self):
        self.assertEqual(self.arg_check.platform_input_checker(self.arg2), Config.ARG_TYPE["general_model"])
        self.assertEqual(self.arg_check.platform_input_checker(self.arg3), Config.ARG_TYPE["model"])
        self.assertEqual(self.arg_check.platform_input_checker(*self.arg7), Config.ARG_TYPE["INVALID"])
        self.assertEqual(self.arg_check.deployment_input_check(*self.arg8), Config.ARG_TYPE["INVALID"])
