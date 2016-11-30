import unittest
import docker
#from ..pyfinder.scanner import Scanner
from pyfinder import Scanner
from pyfinder import ClientSoftware
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

         client_software = ClientSoftware(api_url="http://127.0.0.1:3001/api/software")
         software_to_be_searched= client_software.get_software()
         software_found = image.softwares
         # -2 = scala, groovy is not present
         print(software_to_be_searched)
         self.assertEqual(len(software_to_be_searched) -2,  len(software_found))


        # diunipisocc/dockerfinder:test DOES NOT CONTAIN:
        #      scala,
        #      groovy

        #  sw = [
        #     {'ver': '2.7.12', 'software': 'python'},
        #     {'ver': '1.8.0', 'software': 'java'}, # "1.8.0_111-internal
        #     {'ver': '5.22.2', 'software': 'perl'},
        #     {'ver': '7.51.0', 'software': 'curl'},
        #     {'ver': '2.5.3', 'software': 'nano'},
        #     {'ver': '5.6.28', 'software': 'php'},
        #     {'ver': '2.3.1', 'software': 'ruby'},
        #     {'ver': '2.4.23', 'software': 'httpd'},
        #     {'ver': '1.10.1', 'software': 'nginx'},
        #     {'ver': '8.1.2', 'software': 'pip'},
        #     {'ver': '6.7.0', 'software': 'node'},
        #     {'ver': '3.10.3', 'software': 'npm'},
        #     {'ver': '19.6.0', 'software': 'gunicorn'},
        #     {'ver': '1.18', 'software': 'wget'}
        # ]





if __name__ == '__main__':
    unittest.main()
