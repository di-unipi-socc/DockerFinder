import unittest
from pyfinder import Scanner

class TestScanner(unittest.TestCase):


    def setUp(self):
        self.scanner = Scanner(versions_cmd="../res/versions.yml")


    def test_scan(self):
         dict = self.scanner.scan('mongo-express')

