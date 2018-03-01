import docker
import json
import docker.errors
import re
import logging
import datetime
import sys

from pyfinder.core import ClientImages, ClientHub, ConsumerRabbit, ClientSoftware
from pyfinder.model.image import Image


"""This module contains the source code of the  *Scanner*."""


class Scanner:
    def __init__(self, amqp_url='amqp://guest:guest@127.0.0.1:5672', exchange=None, queue=None, route_key=None,
                 software_url="http://127.0.0.1:3001/api/software",
                 images_url="http://127.0.0.1:3000/api/images",
                 hub_url="https://hub.docker.com/",
                 rmi=True):

        self.rmi = rmi  # remove an image after it is scanned

        self.logger = logging.getLogger(__class__.__name__)
        self.logger.info(__class__.__name__ + " logger  initialized")

        # client of Software service: the service that return the software to
        # search in the images.
        self.client_software = ClientSoftware(api_url=software_url)

        # client of Docker daemon running on the local host
        self.client_daemon = docker.DockerClient(
            base_url='unix://var/run/docker.sock')

        # rabbit consumer of RabbittMQ: receives the images name to scan,
        #   on_message_callback is called when a message is received
        self.consumer = ConsumerRabbit(amqp_url=amqp_url,
                                       exchange=exchange,
                                       queue=queue,
                                       route_key=route_key,
                                       on_msg_callback=self.on_message)

        # client of Images Service:  in order to add and update the images
        self.client_images = ClientImages(images_url=images_url)

        # client of Docker Hub.
        # self.client_hub = ClientHub(docker_hub_endpoint=hub_url)

    def run(self):
        """Start the scanner running the consumer client of the RabbitMQ server."""

        try:
            self.consumer.run()
        except KeyboardInterrupt:
            self.consumer.stop()

    def on_message(self, json_image):
        """
        This is the CALLBACK function that is called when the consumer
        Rabbit receives a message.
        """

        image = Image(from_dict_image=json_image)

        self.logger.info("Received Image {}".format(image))

        # first method called when an image name is received
        attempt = 1
        processed = False
        while attempt < 4 and not processed:
            try:
                self.logger.info("[{}] start scan".format(image.name))
                self.process_repo_name(image)
                processed = True
            except (docker.errors.APIError, docker.errors.NotFound) as e:  # docker.errors.NotFound:
                self.logger.error(str(e) + ": retry number " + str(attempt))
                attempt += 1
            except Exception as e:
                excepName = type(e).__name__ # returns the name of the exception
                self.logger.error(" {} excpetion: {}".format(excepName,str(e)))
                attempt += 1

        if processed is False:
            self.logger.warning("{} - PURGER from the queue after {}"
                                "attempt".format(image.name, attempt))
        return processed

    def process_repo_name(self, image):  # repo_name):
        """
        Process a single image.
        It checks if an image must Scanned or it is already updated.
        """
        self.logger.info(
            "[{}] process repo".format(image.name))
        if self.client_images.is_new(image.name):
            self.logger.info(
                "[{}] is new into local database".format(image.name))
            self.scan(image)
            self.logger.info(
                "[{}] - POST to images server".format(image.name))
            self.client_images.post_image(image.to_dict())

        # TODO: Non chiama Dokcer Hub ???  Ma chima le images serve per capire
        # the image must be scan again
        elif self.client_images.must_scanned(image.name, image.last_updated):
            self.logger.info(
                "[{}] is present into images server but must be scan again".format(image.name))
            self.scan(image)
            #self.logger.info("[{}] - PUT to images server".format(image.name))
            self.client_images.put_image(image.to_dict())  # PUT the new image
            self.logger.info("[{}] - PUT into images server succesfully".format(image.name))
        else:
            self.logger.info(
                "[{}] - uptodate into images server".format(image.name))
        # self.client_daemon.images.remove(image.name, force=True)
        # self.logger.info('[{0}] removed image'.format(image.name))

    #@classmethod
    def scan(self, image):
        """
        It scans an image and create the new Docker finder description.
        """
        # repo_name = image.repo_name
        # tag = image.tag
        # repo_name_tag = image.name

        self.logger.info("[{}] pulling the image ...".format(image.name))

        # for line in self.client_daemon.pull(repo_name, tag, stream=True):
        # json_image=json.loads(line.decode())
        # # self.logger.debug('\r' + json_image['id'] + ":" +
        # # json_image['progress'], end="")
        # if 'status' in json_image.keys() and ("Downloaded" in json_image['status'] or "up to date" in json_image['status']):
        #     self.logger.info(json_image['status'])

        try:
            img = self.client_daemon.images.pull(image.name)

            self.logger.debug('[{0}] start scanning'.format(image.name))

            # search software versions and system commands
            self.logger.info('[{0}] Adding Softwares versions'.format(image.name))
            self.info_dofinder(image)

            # add informatiom from the inspect command
            self.logger.info('[{0}] Adding docker inspect info'.format(image.name))
            self.info_inspect(image)

            self.logger.info('[{0}] finish scanning'.format(image.name))
            image.last_scan = str(datetime.datetime.now())

            # set updated time
            image.set_updated()

            if self.rmi:
                self.client_daemon.images.remove(image.name, force=True)
                self.logger.info('[{0}] removed image'.format(image.name))
        except (docker.errors.APIError, docker.errors.NotFound) as e:
            self.logger.error(str(e))
            self.client_daemon.images.remove(image.name, force=True)

        return image

    def info_dofinder(self, image):
        """
         Extracts the OS distribution and the software versions in the image
        """
        name = image.name

        self.logger.debug('[{}] searching software ... '.format(name))

        # create the container
        entrypoint = "sleep 1000000000"  # "ping 127.0.0.1" | ping -i 10000 127.0.0.1"
        self.logger.debug(
            "[{}] creating container with entrypoint ={}".format(name, entrypoint))

        try:
            container = self.client_daemon.containers.create(
                image=name,
                entrypoint=entrypoint
            )

            # start the container with sleep
            container.start()

            image.softwares = self._extract_softwares(container)

            image.distro = self._extract_distribution(container)

            # search distribution Operating system in the image,
            # self._get_sys(self.versionCommands):
            # for cmd, regex in self.client_software.get_system():
            #     # distro = self.version_from_regex(name, cmd, regex)
            #     distro = self.version_from_regex(container_id, cmd, regex)
            #
            #     if distro:
            #         image.distro = distro

            # after 1 second it stops the container with SIGKILL
            container.stop(timeout=1)
            container.remove(v=True)
            # # search software distribution in the image.
            # softwares = []
            #
            # for sw in self.client_software.get_software():
            #     software = sw['name']
            #     command = software + " " + sw['cmd']
            #     regex = sw['regex']
            #     version = self.version_from_regex(container_id, command, regex)
            #     if version:
            #         softwares.append({'software': software, 'ver': version})
            # image.softwares = softwares

            # stop ping process in the container
            # self.client_daemon.stop(container_id)
        except (docker.errors.ImageNotFound, docker.errors.APIError) as e:
            container.remove(v=True, force=True)
            self.logger.error(str(e))
            raise
        # # remove the contatiner
        # self.client_daemon.remove_container(container_id, force=True, v=True)
        # self.logger.info('[{}] : found {} softwares [{}] '.format(
        #     image.name, len(softwares), softwares))

    def _extract_distribution(self, container):

        for command, regex in self.client_software.get_system():
            res = container.exec_run(cmd=command)
            output = res.decode()
            prog = re.compile(regex)
            match = prog.search(output)
            if match:
                distro = match.group(0)
                self.logger.info("{0} found.".format(distro))
                return distro
            else:
                self.logger.debug("[{0}] NOT found in ".format(command))
        return None


        #     # distro = self.version_from_regex(name, cmd, regex)
        #     distro = self.version_from_regex(container_id, cmd, regex)
        #
        #     if distro:
        #         image.distro = distro



    def _extract_softwares(self, container):
        # list of software distributions found in the image.
        softwares = []
        for sw in self.client_software.get_software():
            # "name":"python", "cmd":"--version", "regex":"[0-9]+\\.[0-9]+(\\.[0-9]+)*"
            command = sw['name']+" " + sw['cmd']
            res = container.exec_run(cmd=command)
            output = res.decode()
            prog = re.compile(sw['regex'])
            match = prog.search(output)
            if match:
                version = match.group(0)
                if version != "." or version != ".go":
                    softwares.append({'software': sw['name'], 'ver': version})
                    self.logger.debug("{0} {1} found.".format(sw['name'], version))
            else:
                self.logger.debug("[{0}] NOT found in ".format(sw['name']))
        self.logger.info('['+''.join('{} {},'.format(s['software'],s['ver']) for s in softwares)+"]")

        return softwares

    def info_inspect(self, image):
        self.logger.debug('[{}] $docker inspect <image>'.format(image.name))
        client = docker.APIClient(base_url='unix://var/run/docker.sock')
        json_inspect = client.inspect_image(image.name)  # Usign Low-level client docker because docker 2.0 has not "inspect_image" method
        image.inspect_info = json_inspect

    def version_from_regex(self, container_id, command, regex):
        try:
            output = self.run_command(container_id, command)
            self.logger.info(regex)
            p = re.compile(regex)
            match = p.search(output)
            if match:
                version = match.group(0)
                if version != "." or version != ".go":
                    self.logger.debug(
                        "[{0}] found in {1}".format(command, container_id))
                    return version
                else:
                    return None
            else:
                self.logger.debug(
                    "[{0}] NOT found in {1}".format(command, container_id))
                return None
        except docker.errors.NotFound as e:
            self.logger.debug(command + " not found")
            # raise
        # except docker.errors.NotFound as e:
        #     self.logger.error(e)
        #     #raise

    def run_command(self, container_id, command):
        """Just like 'docker run CMD'.
            Return the output of the command.i
        """

        self.logger.debug(
            "[{0}] running command {1}".format(container_id, command))

        created_exec = self.client_daemon.exec_create(
            container_id, cmd=command)

        output = self.client_daemon.exec_start(created_exec['Id'])

        #
        # container_id = self.client_daemon.create_container(image=repo_name,
        #                                                    entrypoint=command,
        #                                                    #tty=True,
        #                                                    #stdin_open=True,
        #                                                  )['Id']
        # try:
        #     response =self.client_daemon.start(container=container_id)
        #
        #     self.client_daemon.wait(container_id)
        #
        # except docker.errors.NotFound as e:
        #     self.client_daemon.remove_container(container_id,force=True, v=True)
        #     self.logger.debug(container_id +": ERROR so we have removed")
        #
        # output = self.client_daemon.logs(container=container_id)
        # self.client_daemon.remove_container(container_id,force=True, v=True)
        # self.logger.debug(container_id +": Removed container")

        return output.decode()
