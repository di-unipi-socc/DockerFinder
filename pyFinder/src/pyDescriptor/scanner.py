import docker
import re
import yaml
import os
import datetime
from .container import Container
from .utils import *


class Scanner:

    def __init__(self, versions_cmd="/../../resources/versions.yml"):
        # path of the file containing the command of versions
        self.versionCommands = yaml.load(open(os.path.dirname(__file__) + versions_cmd))
        # sets the docker host from your environment variables
        self.client = docker.Client(**docker.utils.kwargs_from_env(assert_hostname=False))

    def scan(self, repo_name, tag="latest", rmi=False):
        pull_image(repo_name, tag)

        image = {}
        print('Scanning [{0}]'.format(repo_name))
        #image = Image(repo_name_tag=repo_name)

        image['repo_name'] = repo_name
        #image['_id'] = repo_name
        self.info_inspect(repo_name,image)
        self.info_docker_hub(repo_name,image)
        self.info_dofinder(repo_name,image)

        #image.t_scan = datetime.datetime.now()
        image['t_scan'] = str(datetime.datetime.now())

        if rmi:
            remove_image(repo_name, force=True)
        return image

    def info_inspect(self, repo_name, image):
        """
         docker inspect IMAGE
        """
        print('[{}] docker inspect ... '.format(repo_name))
        dict_inspect = self.client.inspect_image(repo_name)
        image['size'] = dict_inspect['Size']
        #image.size = str(dict_inspect['Size'])

    def info_docker_hub(self, repo_name, image):
        # info from Docker API/Search info (size, stars, pulls)
        print('[{}] docker API ... '.format(repo_name))

    def info_dofinder(self, repo_name, image):

        print('[{}] searching binaries version ... '.format(repo_name))

        with Container(repo_name) as c:
            # search distribution
            for cmd, reg in self._get_sys(self.versionCommands):
                output = c.run(cmd)
                p = re.compile(reg)
                match = p.search(output)
                if match:
                    # take the non-capturing group: only the matches, group[0] return all the match
                    dist = match.group(0)
                    #image.distro = dist
                    image['distro'] = dist
                else:
                    print("[{0}] not found {1}".format(repo_name, cmd))

            # search binary versions
            bins = []
            for bin, cmd, regex in self._get_bins(self.versionCommands):
                #print("[{}] searching {} ".format(image, bin))
                output = c.run(bin+" "+cmd)
                p = re.compile(regex)     # can be saved the compilatiion of the regex to savee time (if is equal to all the version)
                match = p.search(output)
                if match:
                    version = match.group(0)
                    print("[{0}] found {1}".format(repo_name, bin))
                    #b = Bin(bin=bin, ver=version)
                    #image.bins.append(b)
                    bins.append({'bin':bin,'ver':version})
                #else:
                #    pass
                #    print("[{0}] not found {1}".format(repo_name, bin))
            image['bins'] = bins
            print('[{}] finish search'.format(repo_name))

    def _get_sys(self, yml_cmd):
        apps = yml_cmd['system']
        for app in apps:
            yield app["cmd"], app["re"]

    def _get_bins(self, yml_cmd):
        apps = yml_cmd['applications']
        for app in apps:
            yield app["name"], app["ver"], app["re"]
