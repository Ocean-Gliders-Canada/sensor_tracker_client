import unittest
from sensor_tracker_api.api import AccessApi


class TestInputChecker(unittest.TestCase):
    """
    those tests deign for local sensor tracker test server
    """

    def setUp(self):
        self.api = AccessApi(debug=True)
        self.general_mode1 = "slocum"
        self.general_mode2 = "wave"
        self.slocum_deployment_list = [58, 59, 73, 77, 80, 78, 75, 74, 71, 70, 69, 66, 63, 62, 60, 57, 56, 55, 53, 51,
                                       50,
                                       48,
                                       47, 45, 44, 43, 41, 39, 38, 36, 35, 34, 33, 32, 31, 30, 29, 28, 27, 26, 25, 24,
                                       23,
                                       22, 21,
                                       19,
                                       18, 17, 16, 15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 82, 83]
        self.wave_deployment_list = [81, 79, 76, 72, 68, 65, 64, 61, 54, 52, 49, 46, 42, 40, 20]

    def testGetDeploymentByGeneralModel(self):
        data_obj = self.api.get_deployments(self.general_mode1)
        data_dict = data_obj.to_dict()
        slocum_deployment_list = self.slocum_deployment_list
        count = 0
        empty_list = []
        for data in data_dict:
            if data["deployment_number"] in slocum_deployment_list:
                if data["deployment_number"] not in empty_list:
                    empty_list.append(data["deployment_number"])
                    count = count + 1
            else:
                pass

        self.assertEqual(66, count)

        data_dict2 = self.api.get_deployments(self.general_mode2).to_dict()
        wave_deployment_list = self.wave_deployment_list
        wave_count = 0
        for data in data_dict2:
            if data["deployment_number"] in wave_deployment_list:
                if data["deployment_number"] not in empty_list:
                    empty_list.append(data["deployment_number"])
                    wave_count = wave_count + 1

            else:
                pass

        self.assertEqual(len(wave_deployment_list), wave_count)

    def testGetDeploymentByMode(self):
        data_dict1 = self.api.get_deployments("Slocum Glider G3").to_dict()
        data_dict2 = self.api.get_deployments("Wave Glider SV2").to_dict()
        slocumG3_count = 0
        slocumG3_list = [83, 82]
        for data in data_dict1:
            if data["deployment_number"] in slocumG3_list:
                slocumG3_count = slocumG3_count + 1

        self.assertEqual(len(slocumG3_list), slocumG3_count)

        wave_deployment_list = self.wave_deployment_list
        wave_count = 0
        for data in data_dict2:
            if data["deployment_number"] in wave_deployment_list:
                wave_count = wave_count + 1

            else:
                pass
        self.assertEqual(len(wave_deployment_list), wave_count)

    def testGetDeploymentByPlatformName(self):
        data_dict = self.api.get_deployments("bond").to_dict()
        bond_list = [73, 77]
        bond_count = 0
        for data in data_dict:
            if data["deployment_number"] in bond_list:
                bond_count = bond_count + 1

        self.assertEqual(len(bond_list), bond_count)

    def testGetDeploymentBynumberOrNameTime(self):
        data_dict1 = self.api.get_deployments("1").to_dict()
        data_dict2 = self.api.get_deployments(1).to_dict()
        data_dict3 = self.api.get_deployments("otn200", "2011-05-13 12:57:00").to_dict()

        self.assertEqual(data_dict1, data_dict2)
        self.assertEqual(data_dict3, data_dict2)
        self.assertEqual(data_dict3[0]["platform_name"], "otn200")
        self.assertEqual(data_dict3[0]["deployment_number"], 1)
