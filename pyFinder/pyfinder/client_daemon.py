import docker
import json
import sys

class ClientDaemon():

    def __init__(self):
        # client = docker.Client(**docker.utils.kwargs_from_env(assert_hostname=False))
        self.client = docker.Client(base_url='unix://var/run/docker.sock')

    def pull_image(repo_name, tag="latest"):
        # sets the docker host from your environment variables
        # client = docker.Client(**docker.utils.kwargs_from_env(assert_hostname=False))
        client = docker.Client(base_url='unix://var/run/docker.sock')
        # try to set image
        if not repo_name:
            ims = client.images()
            if len(ims) >= 1:
                repo_name = [im['RepoTags'][0] for im in client.images()][0]

        assert repo_name, 'No image given or found locally.'

        # get image if not available locally
        im_names = [im['RepoTags'][0] for im in client.images()]  # all the images in the host (first tag)

        if (not any([repo_name in imname for imname in im_names])) and client.search(
                repo_name):  # not found locally and found remote
            print('Image {} not found locally. Pulling from docker hub...'.format(repo_name))
            for line in client.pull(repo_name, tag, stream=True):
                json_image = json.loads(line.decode())
                # print(json_image)
                if 'progress' in json_image.keys():
                    print('\r' + json_image['id'] + ":" + json_image['progress'], end="")
                if 'status' in json_image.keys() and "Downloaded" in json_image['status']:
                    print("\n" + repo_name + ":" + json_image['status'])
        else:
            print("[" + repo_name + "] already exists")

    def remove_image(self, image, force=False):
        print('Removing {} form local docker'.format(image))
        try:
            self.client.remove_image(image, force)
        except:
            e = sys.exc_info()[0]