import unittest
from pyfinder import Scanner

class TestCScanner(unittest.TestCase):


    def setUp(self):
        self.scanner = Scanner(versions_cmd="../res/versions.yml")


    def test_scarn(self):
         dict = self.scanner.scan('ianbr/ebase-data')

