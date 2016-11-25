import unittest
import docker
#from ..pyfinder.scanner import Scanner
from pyfinder import Scanner
from pyfinder import Image
import os

class TestScanner(unittest.TestCase):

    def setUp(self):
        self.scanner = Scanner()

    def test_scan(self):
         client_daemon = docker.Client(base_url='unix://var/run/docker.sock')
         path_dockerfile =  os.path.dirname(os.path.abspath(__file__))
         print(path_dockerfile)
         client_daemon.build(path=path_dockerfile,dockerfile="Dockerfile_test_scanner", tag="diunipisocc/dockerfinder:test")

         image = Image()
         image.name =  "diunipisocc/dockerfinder:test"
         self.scanner.info_dofinder(image)
         print("Out " + str(image.softwares))



if __name__ == '__main__':
    unittest.main()
