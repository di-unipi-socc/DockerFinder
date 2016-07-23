import unittest
#from ..pyfinder.scanner import Scanner
from  pyfinder import ClientSoftware


class TestSoftware(unittest.TestCase):

    def setUp(self):
        self.client = ClientSoftware(host_service="http://127.0.0.1", port_service="3001", path_api="/api/software")#versions_cmd="../../resource/versions.yml")

    def test_scan(self):
         dict = self.client.get_software()
         print(dict)


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
