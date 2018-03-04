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

    def process_repo_name(self, image):
        """
        Process a single image.
        It checks if an image must Scanned or it is already updated.
        """
        self.logger.debug(
            "[{}] process repo".format(image.name))
        if self.client_images.is_new(image.name):
            self.logger.info(
                "[{}] is new into local database".format(image.name))
            self.scan(image)
            self.client_images.post_image(image.to_dict())
            self.logger.info(
                "[{}] - added to images server succesfully".format(image.name))

        # TODO: Non chiama Dokcer Hub ???  Ma chima le images serve per capire the image must be scan again
        elif self.client_images.must_scanned(image.name, image.last_updated):
            self.logger.info(
                "[{}] is present into images server but must be scan again".format(image.name))
            self.scan(image)
            #self.logger.info("[{}] - PUT to images server".format(image.name))
            self.client_images.put_image(image.to_dict())  # PUT the new image
            self.logger.info("[{}] - updated into images server succesfully".format(image.name))
        else:
            self.logger.info(
                "[{}] - uptodate into images server".format(image.name))

    def scan(self, image):
        """
        It scans an image and create the new Docker finder description.
        """
        # repo_name = image.repo_name
        # tag = image.tag
        # repo_name_tag = image.name

        self.logger.info("[{}] pulling the image ...".format(image.name))

        try:
            img = self.client_daemon.images.pull(image.name)

            self.logger.debug('[{0}] start scanning'.format(image.name))

            # search software versions and system commands
            self.logger.info('[{0}] extracing softwares versions ...'.format(image.name))
            self.info_dofinder(image)

            # add informatiom from the inspect command
            self.logger.info('[{0}] adding docker inspect info....'.format(image.name))
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
            container.stop(timeout=1)

            container.remove(v=True)
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
        self.logger.info("{} software found".format(len(softwares)))
        self.logger.debug('Software found: ['+''.join('{} {},'.format(s['software'],s['ver']) for s in softwares)+"]")
        return softwares

    def info_inspect(self, image):
        # "inspect_info":{
        #       "Id":"sha256:702ffd5274797d4cf4b47ac9f4d48cc470ebed1c668a0a2f7e7f1ef493210a65",
        #       "RepoTags":[ ],
        #       "RepoDigests":[ ],
        #       "Parent":"",
        #       "Comment":"",
        #       "Created":"2018-02-26T10:59:06.882767996Z",
        #       "Container":"aaaa08869053814f0a37c5829f74f64f0d5b781e3527572addddf861e5b20376",
        #       "ContainerConfig":{ },
        #       "DockerVersion":"17.06.1-ce",
        #       "Author":"",
        #       "Config":{ },
        #       "Architecture":"amd64",
        #       "Os":"linux",
        #       "Size":374134402,
        #       "VirtualSize":374134402,
        #       "GraphDriver":{ },
        #       "RootFS":{ }
        #    }
        self.logger.debug('[{}] $docker inspect <image>'.format(image.name))
        client = docker.APIClient(base_url='unix://var/run/docker.sock')
        json_inspect = client.inspect_image(image.name)  # Usign Low-level client docker because docker 2.0 has not "inspect_image" method
        wanted_keys = ['Id', 'RepoTags', 'RepoDigests', "Parent", "DockerVersion", "Size",
        "GraphDriver","RootFS", "VirtualSize","Architecture","Os"] # The keys you want
        image.inspect_info  = dict((k, json_inspect[k]) for k in wanted_keys if k in json_inspect)
        # image.inspect_info = json_inspect

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

    def run_command(self, container_id, command):
        """Just like 'docker run CMD'.
            Return the output of the command.i
        """

        self.logger.debug(
            "[{0}] running command {1}".format(container_id, command))

        created_exec = self.client_daemon.exec_create(
            container_id, cmd=command)

        output = self.client_daemon.exec_start(created_exec['Id'])
        return output.decode()
