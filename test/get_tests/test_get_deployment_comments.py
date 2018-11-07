import unittest
from sensor_tracker_api.api import AccessApi


class TestGetDeploymentComments(unittest.TestCase):
    """
    those tests deign for local sensor tracker test server
    """

    def setUp(self):
        self.api = AccessApi(debug=True)
        self.user = "pye"
        self.comment_number = 1
        self.deployment_number = 5
        self.comment_content = "This mission was ended prematurely due to glider leak."

    def testGetDeploymentComments(self):
        data_dict1 = self.api.get_deployment_comments("otn200", "2011-08-24 12:25:00").to_dict()
        data_dict2 = self.api.get_deployment_comments(5).to_dict()
        self.assertEqual(data_dict1,data_dict2)
        self.assertEqual(data_dict1[0]["user__username"], self.user)



