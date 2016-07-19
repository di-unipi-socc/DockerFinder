import docker
import json
import sys


class ClientDaemon(docker.Client):

    def __init__(self, base_url=None, version=None, timeout=60, tls=False):
        super(ClientDaemon, self).__init__(base_url=base_url, version=version, timeout=timeout, tls=tls)
        #base_url = None, version = None,
        #timeout = constants.DEFAULT_TIMEOUT_SECONDS, tls = False
        # client = docker.Client(**docker.utils.kwargs_from_env(assert_hostname=False))
        # client = docker.Client(base_url='unix://var/run/docker.sock')

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
            print('Image {} not found locally. Pulling from docker hub...'.format(repo_name))
            for line in self.pull(repo_name, tag, stream=True):
                json_image = json.loads(line.decode())
                # print(json_image)
                if 'progress' in json_image.keys():
                    print('\r' + json_image['id'] + ":" + json_image['progress'], end="")
                if 'status' in json_image.keys() and "Downloaded" in json_image['status']:
                    print("\n" + repo_name + ":" + json_image['status'])
        else:
            print("[" + repo_name + "] already exists or not found int the Docker Hub")

    def remove_image(self, image, force=False):
        print('Removing {} form local docker'.format(image))
        try:
            self.remove_image(image, force)
        except :
            e = sys.exc_info()[0]

    def __enter__(self, image,  memory_limit_gb=4, stderr=True, stdout=True, volumes=[], cleanup=False, environment=[]):
        """Power on."""

        volumes = [x[1] for x in map(lambda vol: vol.split(':'), volumes)]
        self.cleanup = cleanup  # used to clean up whrn the clientDaemon is out of scope

        self.container_id = self.create_container(
            image=self.image,
            volumes=self.volumes,
            host_config=self.create_host_config(
                binds=volumes,
                mem_limit=int(memory_limit_gb * 1e9)
            ),
            environment=self.environment,
            stdin_open=True,
        )['Id']

        self.start(self.container_id)

        return self

    def __exit__(self, type, value, traceback):
        """Power off."""
        # stop the container when 'with' statement goes out og scope
        self.stop(self.container_id)
        if self.cleanup:
            self.remove_container(self.container_id)

    def run(self, command):
        """Just like 'docker run CMD'.
        This is a generator that yields lines of container output.
        """

        list_of_dict_status = self.containers(filters={'id': self.container_id})
        if not list_of_dict_status or list_of_dict_status[0]['State'] is not 'running':
            self.start(self.container_id)
        exec_id = self.exec_create(
                    container=self.container_id,
                    cmd=command,
                    stdout=self.stdout,
                    stderr=self.stderr,
            )['Id']

        ret = self.exec_start(exec_id, stream=False).decode()
