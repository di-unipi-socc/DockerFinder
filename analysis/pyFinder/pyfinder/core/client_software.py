import requests
import logging

""" This module interacts with the *Software service* running in the *discovery* part."""

class ClientSoftware(requests.Session):

    def __init__(self, api_url="http://127.0.0.1:3001/api/software"): #,host_service="sw_server", port_service="3001", path_api="/api/software"):
        super(ClientSoftware, self).__init__()
        self._url = api_url
        self.logger = logging.getLogger(__class__.__name__)
        self.logger.info(__class__.__name__ + " logger  initialized")
        self.logger.info("SOFTWARE server: " + self._url)

    def get_software(self):
        """Get the list of software. \n
        A software is described by: the name, the version command, and the regex. \n
        E.g. ["python", "--version", '[0-9]*\.[0-9]*[a-zA-Z0-9_\.-]*' ]
        """
        try:
            res = self.get(self._url)
            if res.status_code == requests.codes.ok:
                json_response = res.json()
                self.logger.info(str(json_response['count'])+ " softwares received")
                #software_list = json_response['software'] # list of object
                software_list = json_response['software'] # list of object
                return software_list
        except requests.exceptions.ConnectionError:
            self.logger.exception("ConnectionError: ")
            raise

    def get_system(self):
        """Get the command to know the linux distribution of an image."""
        self.logger.debug("System commands requested")
        d = (('bash -c "cat /etc/*release"', '(?<=PRETTY_NAME=")[^"]*'),
             ('bash -c "lsb_release -a"', 'Description:.*'))

        for l in d:
            yield l[0], l[1]

    def post_software(self, dict_software):
        """Add a software."""
        try:
            res = self.post(self._url, headers={'Content-type': 'application/json'}, json=dict_software)
            if res.status_code == requests.codes.created or res.status_code == requests.codes.ok:
                self.logger.debug("POST [" + dict_software['name'] + "]  into  " + res.url)
            else:
                self.logger.error(str(res.status_code) + " response: " + res.text)
        except requests.exceptions.ConnectionError as e:
            self.logger.exception("ConnectionError: ")
        except:
            self.logger.exception("Unexpected error:")
