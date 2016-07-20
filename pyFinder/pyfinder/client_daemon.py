import docker
import json
import sys
from .utils import get_logger
import logging


class ClientDaemon(docker.Client):

    def __init__(self, base_url=None, version=None, timeout=60, tls=False):
        super(ClientDaemon, self).__init__(base_url=base_url, version=version, timeout=timeout, tls=tls)

        self.logger = get_logger(__name__, logging.INFO)

    def pull_image(self, repo_name, tag="latest"):
        # try to set image
        if not repo_name:
            ims = self.images()
            if len(ims) >= 1:
                repo_name = [im['RepoTags'][0] for im in self.images()][0]

        assert repo_name, 'No image given or found locally.'

        # get image if not available locally
        im_names = [im['RepoTags'][0] for im in self.images()]  # all the images in the host (first tag)

        if (not any([repo_name in imname for imname in im_names])) and self.search(repo_name):  # not found locally and found remote
            self.logger.info('[{0}] not found locally. Pulling from docker hub...'.format(repo_name))
            for line in self.pull(repo_name, tag, stream=True):
                json_image = json.loads(line.decode())
                # print(json_image)
                if 'progress' in json_image.keys():
                    print('\r' + json_image['id'] + ":" + json_image['progress'], end="")
                if 'status' in json_image.keys() and "Downloaded" in json_image['status']:
                    self.logger.info("\n" + repo_name + ":" + json_image['status'])
        else:
            self.logger.info("[" + repo_name + "] already exists or not found int the Docker Hub")

    def remove_image(self, image, force=False):

        try:
            self.remove_image(image, force)
            self.logger.info('[{0}] removed image'.format(image))
        except :
            e = sys.exc_info()[0]
