import unittest
#from ..pyfinder.scanner import Scanner
from pyfinder import Scanner


class TestScanner(unittest.TestCase):

    def setUp(self):
        self.scanner = Scanner()#versions_cmd="../../resource/versions.yml")

    def test_scan(self):
         dict = self.scanner.scan('library/nginx')

