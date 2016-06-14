import docker
import re
import yaml
import os

from mongoengine import *
from .container import Container
from .model.bin import Bin
from .model.image import Image


class Scanner:

    def __init__(self, alias_db, host='localhost', port=27017, versions_cmd="/../../resources/versions.yml"):
        # path of the file containing the command of versions
        self.versionCommands = yaml.load(open(os.path.dirname(__file__) + versions_cmd))
        # sets the docker host from your environment variables
        self.client = docker.Client(**docker.utils.kwargs_from_env(assert_hostname=False))
        #db connection
        self.host = host
        self.alias_db = alias_db
        connect(alias_db, host=host, port=port)

    def scan(self, image_name, tag="latest"):
        image = Image()
        image.repo_name_tag = image_name

        self.pull_image(image_name, tag)
        self.info_inspect(image)
        self.info_docker_hub(image)
        self.info_dofinder(image)

        image.save()
        print('Image {0} scan result stored into database {1}'.format(image_name,self.host+"/"+self.alias_db))

        return image



    def pull_image(self, image_name, tag="latest"):
        # try to set image
        if not image_name:
            ims = self.client.images()
            if len(ims) >= 1:
                image_name = [im['RepoTags'][0] for im in self.client.images()][0]

        assert image_name, 'No image given or found locally.'

        # get image if not available locally
        im_names = [im['RepoTags'][0] for im in self.client.images()]
        if (not any([image_name in imname for imname in im_names])) and self.client.search(image_name):
            print('Image {} not found locally. Pulling from docker hub.'.format(image_name))
            for line in self.client.pull(image_name, stream=True):
                print(line.decode())

    def info_inspect(self, Image):
        """
            docker inspect IMAGE

            dict_info[cfg.ID] = dict_inspect[ID_INSPECT]
            dict_info[cfg.TAGS] = dict_inspect[cfg.TAGS]
            if(dict_inspect[PARENT]): dict_info[PARENT] = dict_inspect[PARENT]
            if(dict_inspect[COMMENT]):dict_info[COMMENT] = dict_inspect[COMMENT]
            dict_info[ROOT_FS] = dict_inspect[ROOT_FS]
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
