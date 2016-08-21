import requests
import logging
from .utils import get_logger


class ClientSoftware(requests.Session):

    def __init__(self, api_url="http://127.0.0.1:3001/api/software"): #,host_service="sw_server", port_service="3001", path_api="/api/software"):
        super(ClientSoftware, self).__init__()
        self._url = api_url
        self.logger = get_logger(__name__, logging.INFO)
        self.logger.info("URL SOFTWARE service: " + self._url)

    def get_software(self):
        try:
            res = self.get(self._url)
            if res.status_code == requests.codes.ok:
                json_response = res.json()
                self.logger.info(str(json_response['count'])+ " softwares received")
                software_list = json_response['software'] # list of object
                return software_list
        except requests.exceptions.ConnectionError:
            self.logger.exception("ConnectionError: ")
            raise

        # d = (("python", "--version", '[0-9]*\.[0-9]*[a-zA-Z0-9_\.-]*'),
        #      ("python3", "--version", '[0-9]*\.[0-9]*[a-zA-Z0-9_\.-]*'),
        #      ("python2", "--version", '[0-9]*\.[0-9]*[a-zA-Z0-9_\.-]*'),
        #      ("java", "-version", '[0-9]*\.[0-9]*[a-zA-Z0-9_\.-]*'),
        #      ("curl", "--version", '[0-9]*\.[0-9]*[a-zA-Z0-9_\.-]*'),
        #      ("nano", "-version", '[0-9]*\.[0-9]*[a-zA-Z0-9_\.-]*'),
        #      ("node", "--version", '[0-9]\.[0-9](\.[0-9])*[^\s]*'),
        #      ("ruby", "--version",'[0-9]\.[0-9](\.[0-9])*[^\s]*'),
        #      ("perl", "-version",'[0-9]\.[0-9](\.[0-9])'))
        # for l in d:
        #     yield l[0], l[1], l[2]

    def get_system(self):
        # - {cmd: 'bash -c "cat /etc/*release"', re: '(?<=PRETTY_NAME=")[^"]*'}  # PRETTY_NAME=.*'
        # - {cmd: 'bash -c "lsb_release -a"', re: 'Description:.*'}
        self.logger.info("System commands requested")
        d = (('bash -c "cat /etc/*release"', '(?<=PRETTY_NAME=")[^"]*'),
             ('bash -c "lsb_release -a"', 'Description:.*'))

        for l in d:
            yield l[0], l[1]

    def post_software(self, dict_software):
        try:
            res = self.post(self._url, headers={'Content-type': 'application/json'}, json=dict_software)
            if res.status_code == requests.codes.created or res.status_code == requests.codes.ok:
                self.logger.info("POST [" + dict_software['name'] + "]  into  " + res.url)
            else:
                self.logger.error(str(res.status_code) + " response: " + res.text)
        except requests.exceptions.ConnectionError as e:
            self.logger.exception("ConnectionError: ")
        except:
            self.logger.exception("Unexpected error:")