import unittest
from sensor_tracker_api.api import AccessApi


class TestGetPlatform(unittest.TestCase):
    """
    those tests deign for local sensor tracker test server
    """

    def setUp(self):
        self.api = AccessApi(debug=True)
        self.general_mode1 = "slocum"
        self.general_mode2 = "wave"
        self.mode1 = "Slocum Glider G1"
        self.slocums = ["Fundy", "dal556", "pearldiver", "otn201", "otn200", "bond", "we10", "we04", "otn121"]

    def testGetPlatform(self):
        data_dict1 = self.api.get_platform(self.general_mode1).to_dict()
        count = 0
        for data in data_dict1:
            if data["name"] in self.slocums:
                count = count+1

        self.assertEqual(9, count)


        data_dict2 = self.api.get_platform(self.mode1).to_dict()
        count = 0
        for data in data_dict2:
            if data["name"] in self.slocums:
                count = count+1

        self.assertEqual(4, count)