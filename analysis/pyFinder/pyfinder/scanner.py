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

        # client of Software service: the service that return the software to search in the images.
        self.client_software = ClientSoftware(api_url=software_url)

        # client of Docker daemon running on the local host
        #self.client_daemon = ClientDaemon(base_url='unix://var/run/docker.sock')
        self.client_daemon = docker.Client(base_url='unix://var/run/docker.sock')

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

    def run(self):
        """Start the scanner running the consumer client of the RabbitMQ server."""

        try:
            self.consumer.run()
        except KeyboardInterrupt:
            self.consumer.stop()

    def on_message(self, json_message):
        """
        This is the CALLBACK function that is called when the consumer Rabbit receives a message.
        """
        self.logger.debug("Received message:" + str(json_message))

        # first method called when an image name is received
        attempt = 1
        processed = False
        while attempt < 4 and not processed:
            try:
                self.logger.debug("["+ json_message['name']+ "] scanning ...")
                self.process_repo_name(json_message)
                processed = True
            except docker.errors.NotFound as e: # docker.errors.NotFound:
                self.logger.error(str(e) +": retry number "+ str(attempt))
                attempt +=1
            except docker.errors.APIError as e:
                self.logger.error(str(e) +": retry number "+ str(attempt))
                attempt +=1

        # self.logger.error("Unexpected error: "+str(sys.exc_info()[0]))
        # self.logger.error("["+json_message['name']+"] processing attempt number: "+ str(attempt))
        # attempt +=1

        if not processed:
            self.logger.warning("["+json_message['name']+"] PURGED from the queue")
        return processed

    def process_repo_name(self, json_image) :#repo_name):
        """
        Process a single image.
        It checks if an image must Scanned or it is already updated.
        """
        # "star_count": 1148,
        # "pull_count": 19432547,

        # "repo_owner": null,
        # "short_description": "GitLab Community Edition docker image based on the Omnibus package",
        # "is_automated": true,
        # "is_official": false,
        # "repo_name": "gitlab/gitlab-ce",
        # "tag": "nightly",
        # "name": "gitlab/gitlab-ce:nightly",
        # "full_size": 390282144,
        # "images": [{"size": 390282144, "architecture": "amd64", "variant": null, "features": null, "os": "linux", "os_version": null, "os_features": null}],
        # "id": 4253706,
        # "repository": 252439,
        # "creator": 454693,
        # "last_updater": 454693,
        # "last_updated": "2017-05-16T02:32:53.252028Z",
        # "image_id": null,
        #  "v2": true

        #is_offical = repo_name['is_official']
        repo_name = json_image['repo_name']
        tag = json_image['tag']
        repo_name_tag = json_image['name']

        #tags = self.client_hub.get_all_tags(repo_name)

        #for tag in tags :  # for scanning all the tags
        #if 'latest' in tags :
        #    tag = 'latest'
        if self.client_images.is_new(repo_name_tag):  # the image is totally new locally

            image = self.scan(json_image)
            dict_image = image.to_dict()
            self.logger.debug("POST [" + repo_name_tag + "] to images server...")
            self.client_images.post_image(dict_image)  # POST the description of the image

            if
        # TODO: Non chiama Dokcer Hub ???  Ma chima le images serve per capire
        # elif self.client_images.must_scanned(repo_name_tag):  # the image must be scan again
        #     self.logger.debug("[" + repo_name_tag+ "] is present into images server but must be scan again")
        #     image = self.scan(json_image)
        #     dict_image = image.to_dict()
        #     self.logger.info("PUT [" + repo_name_tag + "] to images server ...")
        #     self.client_images.put_image(dict_image)  # PUT the new image description of the image
        else:
             # TODO
            self.logger.info("[" + repo_name_tag + "] already up to date.")
        #         self.client_daemon.remove_image(image.name, force=True)
        #         self.logger.info('[{0}] removed image'.format(image.name))


    #@classmethod
    def scan(self, json_image):
        """
        It scans an image and create the new Docker finder description.
        """

        repo_name = json_image['repo_name']
        tag = json_image['tag']
        repo_name_tag = json_image['name']

        self.logger.info("[" + repo_name+":"+tag + "] pulling the image ...")
        for line in self.client_daemon.pull(repo_name, tag, stream=True):
            json_image = json.loads(line.decode())
            # self.logger.debug('\r' + json_image['id'] + ":" + json_image['progress'], end="")
            if 'status' in json_image.keys() and ("Downloaded" in json_image['status'] or "up to date"  in json_image['status']):
                self.logger.info(json_image['status'])

        image = Image()

        image.name = repo_name_tag
        image.tag = tag
        iamge.repo_name = repo_name

        self.logger.debug('[{0}] start scanning'.format(image.name))

        # add info from DockerHub

        #self.logger.info('[{0}] Adding Docker Hub info'.format(image.name))
        #INFO FROM CRAWLER
        #image.user =json_image["creator"]           # String
        if 'star_count' in json_image:
            image.stars = json_image["star_count"]

        if 'pull_count' in json_image:
            image.pulls = json_image["pull_count"]

        if 'description' in json_image:
            image.description = json_image["short_description"]    # String

        if "is_automated" in json_image:

            image.is_automated = json_image["is_automated"]      # Bool

        if "is_official" in json_image:
            image.is_official  = json_image["is_official"]



        self.info_docker_hub(image)



        #image.is_private =json_image[]         # Bool

        # search software versions and system commands
        self.logger.info('[{0}] Adding Softwares versions'.format(image.name))
        self.info_dofinder(image)
        # add informatiom from the inspect command
        self.logger.info('[{0}] Adding docker inspect info'.format(image.name))
        self.info_inspect(image)

        self.logger.info('[{0}] finish scanning'.format(image.name))
        image.last_scan = str(datetime.datetime.now())

        image.set_updated()
        if self.rmi:
            try:
                self.client_daemon.remove_image(image.name, force=True)
                self.logger.info('[{0}] removed image'.format(image.name))
            except docker.errors.APIError as e:
                self.logger.error(str(e))
            except docker.errors.NotFound as e:
                self.logger.error(str(e))

        return image

    def info_docker_hub(self,image):
        """Get the informations of an image from Docker Hub."""
        self.logger.debug('[{}] adding Docker Hub info ... '.format(image.name))

        repo_name  = image.name.split(":")[0]
        tag        = image.name.split(":")[1]

        # json_response = self.client_hub.get_json_repo(repo_name)
        #
        # if json_response:
        #     if 'user' in json_response:
        #         image.user = json_response['user']
        #
        #     if 'star_count' in json_response:
        #         image.stars = json_response['star_count']
        #
        #     if 'pull_count' in json_response:
        #         image.pulls =  json_response['pull_count']
        #
        #     if 'description' in json_response:
        #         image.description = json_response['description']
        #
        #     if "is_automated" in json_response:
        #         image.is_automated =  json_response['is_automated']
        #
        #     if "is_private" in json_response:
        #         image.is_private =  json_response['is_private']

        json_response = self.client_hub.get_json_tag(repo_name, tag, image.is_official)

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

    #@classmethod
    def info_dofinder(self, image):
        """
         Extracts the OS distribution and the software versions in the image
        """
        name = image.name
        self.logger.debug('[{}] searching software ... '.format(name))


        #create the container
        entrypoint = "sleep 1000000000" # "ping 127.0.0.1" | ping -i 10000 127.0.0.1"
        self.logger.debug("[{}] creating container with entrypoint ={}".format(name, entrypoint))
        container_id = self.client_daemon.create_container(
                                                        image=name,
                                                        entrypoint=entrypoint
                                                        )['Id']
        try:
            # start the container
            self.client_daemon.start(container_id)

            # search distribution Operating system in the image,
            for cmd, regex in self.client_software.get_system():  # self._get_sys(self.versionCommands):
                #distro = self.version_from_regex(name, cmd, regex)
                distro = self.version_from_regex(container_id, cmd, regex)
                if distro:
                    image.distro = distro

            # search software distribution in the image.
            softwares = []

            for sw in self.client_software.get_software():
                software = sw['name']
                command = software + " " + sw['cmd']
                regex = sw['regex']
                version = self.version_from_regex(container_id, command, regex)
                if version:
                    softwares.append({'software': software, 'ver': version})
            image.softwares = softwares

            # stop ping process in the container
            self.client_daemon.stop(container_id)
        except :
            self.client_daemon.remove_container(container_id,force=True, v=True)
            raise
        # remove the contatiner
        self.client_daemon.remove_container(container_id,force=True, v=True)
        self.logger.info('[{}] : found {} softwares [{}] '.format(image.name, len(softwares), softwares))

    def info_inspect(self, image):
        self.logger.debug('[{}] $docker inspect <image>'.format(image.name))
        json_inspect = self.client_daemon.inspect_image(image.name)
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
                    self.logger.debug("[{0}] found in {1}".format(command, container_id))
                    return version
                else:
                    return None
            else:
                self.logger.debug("[{0}] NOT found in {1}".format(command, container_id))
                return None
        except docker.errors.NotFound as e:
            self.logger.debug(command + " not found")
            #raise
        # except docker.errors.NotFound as e:
        #     self.logger.error(e)
        #     #raise


    def run_command(self, container_id, command):
        """Just like 'docker run CMD'.
            Return the output of the command.i
        """

        self.logger.debug("[{0}] running command {1}".format(container_id, command))

        created_exec = self.client_daemon.exec_create(container_id, cmd=command)

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
