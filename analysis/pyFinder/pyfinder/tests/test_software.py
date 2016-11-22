import unittest
#from ..pyfinder.scanner import Scanner
from  pyfinder import ClientSoftware


class TestSoftware(unittest.TestCase):

    def setUp(self):
        self.client = ClientSoftware(api_url="http://180.0.0.5:3001/api/software")

    def test_scan(self):
         dict = self.client.get_software()
         print(dict)


    @unittest.skip("ho saltato il test post")
    def test_post(self):
        d = {
            "name": "python3",
            "cmd": "--version",
            "regex": "[0-9]*[.][0-9]*[a-zA-Z0-9_.-]*"
        }
        # }, {
        #     "name": "python2",
        #     "cmd": "--version",
        #     "regex": "[0-9]*[.][0-9]*[a-zA-Z0-9_.-]*"
        # }
        self.client.post_softwaare(d)
