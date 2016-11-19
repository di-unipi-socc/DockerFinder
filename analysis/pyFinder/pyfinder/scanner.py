import docker
import docker.errors
from subprocess import Popen, PIPE, STDOUT
import re
from .utils import *
from .client_images_service import ClientImages
from .client_daemon import ClientDaemon
from .client_dockerhub import ClientHub
from .client_software import ClientSoftware
from .consumer_rabbit import ConsumerRabbit
from .utils import get_logger
from .model.image import Image
import logging
import sys
"""This module contains the *Scanner* implementation."""

class Scanner:
    def __init__(self, amqp_url='amqp://guest:guest@127.0.0.1:5672', exchange=None, queue=None, route_key=None,
                 software_url="http://127.0.0.1:3001/api/software",
                 images_url="http://127.0.0.1:3000/api/images",
                 hub_url="https://hub.docker.com/",
                 rmi=True):


        self.rmi = rmi  # remove an image after it is scanned

        self.logger = get_logger(__name__, logging.INFO)

        # client of Software service: the service that return the software to search in the images.
        self.client_software = ClientSoftware(api_url=software_url)

        # client of Docker daemon running on the local host
        self.client_daemon = ClientDaemon(base_url='unix://var/run/docker.sock')

        # rabbit consumer of RabbittMQ: receives the images name to scan,
        #   on_message_callback is called when a message is received
        self.consumer = ConsumerRabbit(amqp_url=amqp_url,
                                       exchange=exchange,
                                       queue=queue,
                                       route_key=route_key,
                                       on_msg_callback=self.on_message)

        # client of Images Service:  in order to add and update the image description.
        self.client_images = ClientImages(images_url=images_url)

        # client of Docker Hub.
        self.client_hub = ClientHub(docker_hub_endpoint=hub_url)

    def on_message(self, json_message):
        """
        This is the CALLBACK function that is called when the consumer Rabbit receives a message.
        """
        self.logger.info("Received message:" + str(json_message))

        # first method called when an image name is received
        attempt = 1
        processed = False
        while attempt < 4 and not processed:
            try:
                self.process_repo_name(json_message['name'])
                processed = True
            except docker.errors as e:
                self.logger.error(str(e))
                self.logger.error("["+json_message['name']+"] processing attempt number: "+ str(attempt))
                attempt +=1
            # except :
            #     self.logger.error("Unexpected error: "+str(sys.exc_info()[0]))
            #     self.logger.error("["+json_message['name']+"] processing attempt number: "+ str(attempt))
            #     attempt +=1

        #if not processed: self.logger.info("["+json_message['name']+"] PURGED from the queue")
        #return processed

    def run(self):
        """Start the scanner running the consumer client of the RabbitMQ server."""

        try:
            self.consumer.run()
        except KeyboardInterrupt:
            self.consumer.stop()

    def process_repo_name(self, repo_name):
        """Process a single image. It checks if an image must Scanned or it is already updated."""

        tags = self.client_hub.get_all_tags(repo_name)

        #for tag in tags :  # for scanning all the tags
        if 'latest' in tags :
            tag = 'latest'
            if self.client_images.is_new(repo_name):  # the image is totally new
                image = self.scan(repo_name, tag)
                dict_image = image.to_dict()
                self.client_images.post_image(dict_image)  # POST the description of the image
                self.logger.info("[" + dict_image['name'] + "]  POST the image description")
            elif self.client_images.must_scanned(repo_name):  # the image must be scan again
                self.logger.debug("[" + repo_name + "] is present into images server but must be scan again")
                image = self.scan(repo_name, tag)
                dict_image = image.to_dict()
                self.client_images.put_image(dict_image)  # PUT the new image description of the image
                self.logger.info("[" + dict_image['name'] + "] PUT the image description")
            else:
                self.logger.info("[" + repo_name + "] already up to date.")

    def scan(self, repo_name, tag="latest"):
        """It scans an image and create the new Docker finder description. \n

        """
        try:
            self.client_daemon.pull_image(repo_name, tag)
        except docker.errors as e:
            self.logger.exception(e)
            raise

        image = Image()

        image.name = repo_name+":"+tag

        self.logger.info('[{0}] start scanning'.format(image.name))

        # add info from DockerHub
        self.info_docker_hub(image)
        # search software versions and system commands
        self.info_dofinder(image)
        # add informatiom from the inspect command
        self.info_inspect(image)

        self.logger.info('[{0}] finish scanning'.format(image.name))
        image.last_scan = str(datetime.datetime.now())

        image.set_updated()

        if self.rmi:
            try:
                self.client_daemon.remove_image(image.name, force=True)
                self.logger.info('[{0}] removed image'.format(image.name))
            except docker.errors.NotFound as e:
                self.logger.error(e)
        return image

    def info_docker_hub(self,image):
        """Get the informations of an image from Docker Hub."""
        self.logger.info('[{}] adding Docker Hub info ... '.format(image.name))

        repo_name  = image.name.split(":")[0]
        tag        = image.name.split(":")[1]

        json_response = self.client_hub.get_json_repo(repo_name)

        if json_response:
            if 'description' in json_response:
                image.description = json_response['description']

            if 'star_count' in json_response:
                image.stars = json_response['star_count']

            if 'pull_count' in json_response:
                image.pulls =  json_response['pull_count']

        json_response = self.client_hub.get_json_tag(repo_name, tag)

        if 'last_updated' in json_response:
            image.last_updated = json_response['last_updated']

        if 'last_updater'  in json_response:
            image.last_updater = json_response['last_updater']

        if 'full_size' in json_response:
            image.size = json_response['full_size']

        if 'repository' in json_response:
            image.repository = json_response['repository']

        if 'id' in json_response:
            image.id_tag= json_response['id']

        if 'creator' in json_response:
            image.creator = json_response['creator']

    def info_dofinder(self, image):
        """It Extracts the OS distribution and the software in the image"""
        name = image.name
        self.logger.info('[{}] searching software ... '.format(name))

        # search distribution Operating system in the image,
        for cmd, regex in self.client_software.get_system():  # self._get_sys(self.versionCommands):
            try:
                distro = self.version_from_regex(name, cmd, regex)
                if distro:
                    image.distro = distro
                    #dict_image['distro'] = distro
            except docker.errors.NotFound as e:
                self.logger.error(e)

        # search software distribution in the image.
        softwares = []
        for sw in self.client_software.get_software():  #
            try:
                software = sw['name']
                command = software + " " + sw['cmd']
                regex = sw['regex']
                version = self.version_from_regex(name, command, regex)
                if version:
                    softwares.append({'software': software, 'ver': version})
            except docker.errors.NotFound as e:
                self.logger.error(e)
        #dict_image['softwares'] = softwares
        image.softwares = softwares

    def info_inspect(self, image):
        self.logger.info('[{}] $dokcer inspect <image> .format(image.name))
        json_inspect = self.client_daemon.inspect_image(image.name)
        image.inspect_info = json_inspect



    def version_from_regex(self, repo_name, command, regex):

        output = self.run_command(repo_name, command)

        p = re.compile(regex)
        match = p.search(output)
        if match:
            version = match.group(0)
            self.logger.debug("[{0}] found in {1}".format(command, repo_name))
            return version
        else:
            self.logger.debug("[{0}] NOT found in {1}".format(command, repo_name))
            return None


    def run_command(self, repo_name, command):
        """Just like 'docker run CMD'.
        Return the output of the command.
        """

        self.logger.info("[{0}] running command {1}".format(repo_name, command))
        try:
            container_id = self.client_daemon.create_container(image=repo_name,
                                                           entrypoint=command,
                                                           tty=True,
                                                           stdin_open=True,

                                                         )['Id']

            self.client_daemon.start(container=container_id)

            self.client_daemon.wait(container_id)
            output = self.client_daemon.logs(container=container_id)
            self.client_daemon.remove_container(container_id)
            self.logger.debug("Removed container "+container_id)

        # except requests.exceptions.HTTPError as e:
        #     self.logger.error(e)
        #     raise
        except docker.errors.APIError as e:
            self.logger.error(e)
            raise
        # except:
        #     #self.logger.error("Unexpected error:"+str(sys.exc_info()[0]))
        #     raise

        return output.decode()
