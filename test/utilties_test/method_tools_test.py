import unittest
from sensor_tracker_api.utilities.method_tools import call_method


class TestCallMethod(unittest.TestCase):
    def setUp(self):
        self.function_name = "sample_function"
        self.input1 = 1
        self.input2 = "a"
        self.input3 = [1, 2, 3, 4]
        self.input4 = {'wom_id': "", 'deployment_number': 88}

    def testNoInput(self):
        obj = SampleA(self.input1, self.input2)
        res = obj.sample_function()
        except_res = "{a} {b}".format(a=self.input1, b=self.input2)
        self.assertEqual(res, except_res)
        param = None
        res_from_call_method = call_method(self.function_name, obj)
        self.assertEqual(res_from_call_method, except_res)

    def testArrayInput(self):
        obj = SampleB()
        res = obj.sample_function(self.input3)
        except_res = self.input3
        self.assertEqual(res, self.input3)
        param = self.input3
        res_from_call_method = call_method(self.function_name, obj, param=param)
        self.assertEqual(res_from_call_method, except_res)

    def testComplexInput(self):
        obj = SampleC()
        res = obj.sample_function(self.input1, self.input3, c=self.input2)
        except_res = (self.input1, self.input3, self.input2)
        self.assertEqual(res, except_res)
        param = (self.input1, self.input3, self.input2)
        res_from_call_method = call_method(self.function_name, obj, param=param)
        self.assertEqual(res_from_call_method, except_res)

    def testComplexInput2(self):
        obj = SampleD()
        res = obj.sample_function(self.input1, self.input4)
        except_res = (self.input1, self.input4)
        self.assertEqual(res, except_res)
        param = (self.input1, self.input4)
        res_from_call_method = call_method(self.function_name, obj, param=param)
        self.assertEqual(res_from_call_method, except_res)


class SampleA(object):
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def sample_function(self):
        return "{a} {b}".format(a=self.a, b=self.b)


class SampleB(object):

    def sample_function(self, a):
        return a


class SampleC(object):

    def sample_function(self, a, b, c=None):
        return a, b, c


class SampleD(object):

    def sample_function(self, id, content):
        return id, content
