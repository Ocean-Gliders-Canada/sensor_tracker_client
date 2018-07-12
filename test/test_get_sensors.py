import unittest
from sensor_tracker_api.api import AccessApi


class TestGetSensors(unittest.TestCase):
    """
    those tests deign for local sensor tracker test server
    """

    def setUp(self):
        self.api = AccessApi(debug=True)
        self.platform_name = "dal556"
        self.deployment_time = "2017-06-05 15:13:26"

    def testGetOutputSensors(self):
        object_dict1 = self.api.get_sensors(self.platform_name,self.deployment_time).to_dict()
        self.assertEqual(15, len(object_dict1))


    def testGetSensors(self):
        object_dict1 = self.api.get_sensors(self.platform_name, self.deployment_time, output=False).to_dict()
        self.assertEqual(19+15, len(object_dict1))