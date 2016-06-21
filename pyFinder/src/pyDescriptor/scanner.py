import docker
import re
import yaml
import os
import datetime

from .container import Container
from .model.bin import Bin
from .model.image import Image



class Scanner:

    def __init__(self, versions_cmd="/../../resources/versions.yml"):
        # path of the file containing the command of versions
        self.versionCommands = yaml.load(open(os.path.dirname(__file__) + versions_cmd))
        # sets the docker host from your environment variables
        self.client = docker.Client(**docker.utils.kwargs_from_env(assert_hostname=False))

    def scan(self, repo_name, tag="latest"):
        print('Scanning  {0} '.format(repo_name))
        image = Image(repo_name_tag=repo_name)
        self.info_inspect(image)
        self.info_docker_hub(image)
        self.info_dofinder(image)
        image.t_scan = datetime.datetime.now()
        return image

    def info_inspect(self, Image):
        """
         docker inspect IMAGE
        """

        name_tag = Image.repo_name_tag

        print('[{}] docker inspect ... '.format(name_tag))
        dict_inspect = self.client.inspect_image(name_tag)

        Image.size = str(dict_inspect['Size'])

    def info_docker_hub(self, Image):
        # info from Docker API/Search info (size, stars, pulls)
        name_tag = Image.repo_name_tag
        print('[{}] docker API ... '.format(name_tag))


    def info_dofinder(self, Image):
        """
        :param Image: the object representing the image
        :return:  the image enriched with the binary  installed in the image and the distribution
        """
        name_tag = Image.repo_name_tag
        print('[{}] searching binaries version ... '.format(name_tag))

        with Container(name_tag) as c:
            # search distribution
            for cmd, reg in self._get_sys(self.versionCommands):
                output = c.run(cmd)
                p = re.compile(reg)
                match = p.search(output)
                if match:
                    # take the non-capturing group: only the matches, group[0] return all the match
                    dist = match.group(0)
                    Image.distro = dist

                else:
                    print("[{0}] not found {1}".format(name_tag, cmd))
            # search applications versions
            for bin, cmd, regex in self._get_bins(self.versionCommands):
                #print("[{}] searching {} ".format(image, bin))
                output = c.run(bin+" "+cmd)
                p = re.compile(regex)     # can be saved the compilatiion of the regex to savee time (if is equal to all the version)
                match = p.search(output)
                if match:
                    version = match.group(0)
                    b = Bin(bin=bin, ver=version)
                    Image.bins.append(b)
                else:
                    pass
                    print("[{0}] not found {1}".format(name_tag, bin))
            print('[{}] finish search'.format(name_tag))

    def _get_sys(self, yml_cmd):
        apps = yml_cmd['system']
        for app in apps:
            yield app["cmd"], app["re"]

    def _get_bins(self, yml_cmd):
        apps = yml_cmd['applications']
        for app in apps:
            yield app["name"], app["ver"], app["re"]
