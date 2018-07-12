import unittest
from sensor_tracker_api.api import AccessApi


class TestGetInstruments(unittest.TestCase):
    """
    those tests deign for local sensor tracker test server
    """

    def setUp(self):
        self.api = AccessApi(debug=True)
        self.platform_name = "dal556"
        self.instrument_id_on_platform = [16, 17, 11, 23, 22, 24, 28, 25, 27, 26, 28, 24, 11, 15, 27]
        self.deployment_time = "2017-06-05 15:13:26"
        self.instrument_id_on_mission_74 = [16, 17, 25, 26, 11, 15]

    def testGetInstrumentOnPlatform(self):
        obj_dict = self.api.get_instruments(self.platform_name).to_dict()
        count = 0
        for data in obj_dict:
            if data["instrument_id"] in self.instrument_id_on_platform:
                count = count + 1

        self.assertEqual(len(self.instrument_id_on_platform), count)

    def testGetInstrumentByDeploymentNumberOrNameTime(self):
        obj_dict1 = self.api.get_instruments(self.platform_name, self.deployment_time).to_dict()
        obj_dict2 = self.api.get_instruments(74).to_dict()
        self.assertEqual(obj_dict1, obj_dict2)
        count = 0
        for data in obj_dict1:
            if data["id"] in self.instrument_id_on_platform:
                count = count + 1

        self.assertEqual(len(self.instrument_id_on_mission_74), count)
