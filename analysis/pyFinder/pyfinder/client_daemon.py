import docker
import docker.errors
import json
import sys
from .utils import get_logger
import logging


class ClientDaemon(docker.Client):

    def __init__(self, base_url=None, version=None, timeout=60, tls=False):
        #base_url = 'unix://var/run/docker.sock'
        super(ClientDaemon, self).__init__(base_url=base_url, version=version, timeout=timeout, tls=tls)
        self.logger = get_logger(__name__, logging.INFO)

    def pull_image(self, repo_name, tag="latest"):
        """
        The method pulls the image from the Docker Hub.
        :param repo_name: the name of the iamge to pull.
        :param tag: tha tag of the iamge to pull (dafault latest)
        """
        try:
            self.logger.info("[" + repo_name + "] pulling ...")
            for line in self.pull(repo_name, tag, stream=True):
                json_image = json.loads(line.decode())
                # print(json_image)
                if 'progress' in json_image.keys():
                    pass
                    # self.logger.debug('\r' + json_image['id'] + ":" + json_image['progress'], end="")
                if 'status' in json_image.keys() and "Downloaded" in json_image['status']:
                    self.logger.info("[" + repo_name + "] " + json_image['status'])
        except docker.errors as e:
                self.logger.exception(e)
