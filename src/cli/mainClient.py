from src.cli.container import *
from src.utils import utils

import yaml

import docker
import re


SYS = "System"
DST = "Distro"

BINS = "Bins"
BIN = "Bin"
VER = "Ver"


# sets the docker host from your environment variables
client = docker.Client(**docker.utils.kwargs_from_env(assert_hostname=False))

#path file of the ymal file specifiing the commands for extractin  the versions
path_versions_cmd = "/home/dido/github/DockerFinder/resources/versions.yml"

path_json_out = "/home/dido/github/DockerFinder/dofinder.json"


def dofinder(image):

    dict_info = {SYS: {}, BINS: []}

    # try to set image
    if not image:
        ims = client.images()
        if len(ims) >= 1:
            image = [im['RepoTags'][0] for im in client.images()][0]


    assert image, 'No image given or found locally.'

    # get image if not available locally
    imnames = [im['RepoTags'][0] for im in client.images()]
    if (not any([image in imname for imname in imnames])) and client.search(image):
        print('Image {} not found locally. Pulling from docker hub.'.format(image))
        ret = client.pull(image)
        print(ret)





    ### GET THE SYSTEM DISTRI AND THE BINARY RUNNING IN THE CONTAINER
    versionCommands = yaml.load(open(path_versions_cmd))

    with Container(image, cleanup=True) as c:
        #search distribution
        for cmd, reg in getSystemCommand(versionCommands):
            output = c.run(cmd)
            p = re.compile(reg)
            match = p.search(output)
            if match:
                ver = match.group(0)
                dict_info[SYS] = {DST: ver}
                print('[{}] found {}'.format(image, ver))
            else:
                print("[{}] not found {}".format(image, cmd))

        #search applications versions
        for bin, cmd, regex in getVersionCommad(versionCommands):
            print("[{}] searching {} ".format(image, bin))
            output = c.run(bin+" "+cmd)
            p = re.compile(regex)     ## can be saved the compilatiion of the regex to savee time (if is equal to all the version)
            match = p.search(output)
            if match:
                ver = match.group(0)
                dict_info[BINS].append({BIN: bin, VER: ver})
                print('[{}] found {} {}'.format(image, bin, ver))
            else:
                print("[{}] not found {}".format(image, bin))

        utils.dictToJson(path_json_out, dict_info)



def getSystemCommand(ymlCommand):
    apps = ymlCommand['system']
    for app in apps:
        yield app["cmd"], app["re"]


def getVersionCommad(ymlCommand):
    apps = ymlCommand['applications']
    for app in apps:
        yield app["name"], app["ver"], app["re"]



#dofinder("ubuntu")
#dofinder("python")
dofinder("java")

#dofinder("dido/mix")