import docker
import os
import re
import yaml

from pyFinder.conf import cfg
from pyFinder.src.pyDescriptor.container import Container

#ID = "_id"         # put into  conf folder
ID_INSPECT = "Id"
#TAGS = "RepoTags"  # put into  conf folder
PARENT = "Parent"
COMMENT = "Comment"
ROOT_FS = "RootFS"


SYS = "System"
DST = "Distro"

BINS = "Bins"
BIN = "Bin"
VER = "Ver"


# sets the docker host from your environment variables
client = docker.Client(**docker.utils.kwargs_from_env(assert_hostname=False))


#path file of the yaml file specifing the commands for extracting the versions
conf_path = os.path.abspath(os.path.abspath('..'))

path_versions_cmd = os.path.join(conf_path, "cfg.py")
#path_versions_cmd = "../../resources/versions.yml"

print(path_versions_cmd)

def extractInfo(image):

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

    # 1) info from Docker inspect
    print('[{}] docker inspect ... '.format(image))

    dict_inspect = client.inspect_image(image)
    dict_info[cfg.ID] = dict_inspect[ID_INSPECT]
    dict_info[cfg.TAGS] = dict_inspect[cfg.TAGS]
    if(dict_inspect[PARENT]): dict_info[PARENT] = dict_inspect[PARENT]
    if(dict_inspect[COMMENT]):dict_info[COMMENT] = dict_inspect[COMMENT]
    dict_info[ROOT_FS] = dict_inspect[ROOT_FS]

    # 2) info from Docker API/Search info (size, stars, pulls)


    # 3) info distro and applications versions in the image
    print('[{}] searching binaries version ... '.format(image))

    versionCommands = yaml.load(open(path_versions_cmd))

    with Container(image, cleanup=True) as c:
        #search distribution
        for cmd, reg in getSystemCommand(versionCommands):
            output = c.run(cmd)
            p = re.compile(reg)
            match = p.search(output)
            if match:
                ver = match.group(0) # take the non-capturing group: only the matches, group[0] return all the match
                dict_info[SYS] = {DST: ver}
                #print('[{}] found {}'.format(image, ver))
            else:
                pass
                #print("[{}] not found {}".format(image, cmd))

        #search applications versions
        for bin, cmd, regex in getVersionCommad(versionCommands):
            #print("[{}] searching {} ".format(image, bin))
            output = c.run(bin+" "+cmd)
            p = re.compile(regex)     # can be saved the compilatiion of the regex to savee time (if is equal to all the version)
            match = p.search(output)
            if match:
                ver = match.group(0)
                dict_info[BINS].append({BIN: bin, VER: ver})
                #print('[{}] found {} {}'.format(image, bin, ver))
            else:
                pass
                #print("[{}] not found {}".format(image, bin))
        print('[{}] finish search'.format(image))
        return dict_info

def getSystemCommand(ymlCommand):
    apps = ymlCommand['system']
    for app in apps:
        yield app["cmd"], app["re"]


def getVersionCommad(ymlCommand):
    apps = ymlCommand['applications']
    for app in apps:
        yield app["name"], app["ver"], app["re"]
