#!python
# coding=utf-8
import unittest



class TestGetTargetFiles(unittest.TestCase):
    def setUp(self):

        self.platform = "dal556"
        self.time = "2016-01-22 17:26:00"
        self.target_dir = "/Users/xing/Desktop/project/GUTILS_RUN/GUTILS_RUN/test/resource/data"
        self.base_dir = "/Users/xing/Desktop/project/GUTILS_RUN/GUTILS_RUN/test/output"
        self.args = dict(

            time=self.time,
            platform=self.platform,
            base_dir=self.base_dir,
            live=False,
        )

    def testtest(self):
        self.assertEqual(1,1)

if __name__ == '__main__':
    unittest.main()
