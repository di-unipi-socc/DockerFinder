
import docker

# sets the docker host from your environment variables
client = docker.Client(**docker.utils.kwargs_from_env(assert_hostname=False))


class Container:
    """
    Represents a single docker container on the host.

    Volumes should be a list of mapped paths, e.g. ['/var/log/docker:/var/log/docker'].
    """

    def __init__(self, image, memory_limit_gb=4, stderr=True, stdout=True, volumes=[], cleanup=False, environment=[]):
        self.image = image
        self.memory_limit_bytes = int(memory_limit_gb * 1e9)
        self.stderr = stderr
        self.stdout = stdout
        self.volumes = [x[1] for x in map(lambda vol: vol.split(':'), volumes)]
        self.binds = volumes
        self.cleanup = cleanup
        self.environment = environment

    def __enter__(self):
        """Power on."""
        self.container_id = client.create_container(
            image=self.image,
            volumes=self.volumes,
            host_config=client.create_host_config(
                binds=self.binds,
                mem_limit=self.memory_limit_bytes
                ),
            environment=self.environment,
            stdin_open=True
        )['Id']

        client.start(self.container_id)

        return self

    def __exit__(self, type, value, traceback):
        """Power off."""
        # stop the container when 'with' statement goes out og scope
        client.stop(self.container_id)
        if self.cleanup:
            client.remove_container(self.container_id)


    def run(self, command):
        """Just like 'docker run CMD'.
        This is a generator that yields lines of container output.
        """
        exec_id = client.exec_create(
            container=self.container_id,
            cmd=command,
            stdout=self.stdout,
            stderr=self.stderr
        )['Id']

        for line in client.exec_start(exec_id, stream=True):
            yield line

    def pull(image):
        # get image if not available locally
        imnames = [im['RepoTags'][0] for im in client.images()]
        if (not any([image in imname for imname in imnames])) and client.search(image):
            print('Image "{}" not found locally. Pulling from docker hub...'.format(image))
            for line in client.pull(image, stream=True):
                yield line


