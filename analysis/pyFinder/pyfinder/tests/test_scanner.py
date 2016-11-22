import unittest
#from ..pyfinder.scanner import Scanner
from pyfinder import Scanner


class TestScanner(unittest.TestCase):

    def setUp(self):
        self.scanner = Scanner()

    def test_scan(self):
         dicti = self.scanner.scan("nginx", tag="latest")
         print("Out " + str(dicti))



if __name__ == '__main__':
    unittest.main()
