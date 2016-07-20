import json
import docker
import sys
import datetime
import time
import logging

# def pull_image(repo_name, tag="latest"):
#     # sets the docker host from your environment variables
#     #client = docker.Client(**docker.utils.kwargs_from_env(assert_hostname=False))
#     client = docker.Client(base_url='unix://var/run/docker.sock')
#     # try to set image
#     if not repo_name:
#         ims = client.images()
#         if len(ims) >= 1:
#             repo_name = [im['RepoTags'][0] for im in client.images()][0]
#
#     assert repo_name, 'No image given or found locally.'
#
#     # get image if not available locally
#     im_names = [im['RepoTags'][0] for im in client.images()]  # all the images in the host (first tag)
#
#     if (not any([repo_name in imname for imname in im_names])) and client.search(repo_name):  # not found locally and found remote
#         print('Image {} not found locally. Pulling from docker hub...'.format(repo_name))
#         for line in client.pull(repo_name, tag, stream=True):
#             json_image = json.loads(line.decode())
#             #print(json_image)
#             if 'progress' in json_image.keys():
#                 print ('\r' + json_image['id'] + ":" + json_image['progress'], end="")
#             if 'status' in json_image.keys() and "Downloaded" in json_image['status']:
#                 print ("\n"+repo_name+":" +json_image['status'])
#     else:
#         print("[" +repo_name +"] already exists")
#
#
# def remove_image(image, force=False):
#     client = docker.Client(**docker.utils.kwargs_from_env(assert_hostname=False))
#     print('Removing {} form local docker'.format(image))
#     try:
#         client.remove_image(image, force)
#     except:
#         e = sys.exc_info()[0]
#         print(e)


def string_to_date(string_date):
    return datetime.datetime(*time.strptime(string_date, "%Y-%m-%dT%H:%M:%S.%fZ")[:7])


def get_logger(name_class, level):

    logger = logging.getLogger(name_class)
    #logging.basicConfig(level=logging.DEBUG)
    logger.setLevel(logging.DEBUG)

    # create file handler which logs even debug messages
    #fh = logging.FileHandler(name_file)
    #fh.setLevel(level)

    # create console handler with a higher log level
    ch = logging.StreamHandler()
    ch.setLevel(level)

    # create formatter and add it to the handlers
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    #fh.setFormatter(formatter)
    ch.setFormatter(formatter)

    # add the handlers to the logger
    #logger.addHandler(fh)
    logger.addHandler(ch)

    assert isinstance(logger, logging.Logger)
    return logger
