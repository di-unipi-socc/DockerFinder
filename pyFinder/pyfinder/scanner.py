import docker
import docker.errors
import re
import yaml
import os
import datetime
import time
from .container import Container
from .utils import *
from .client_images_service import ClientImages
from .client_daemon import ClientDaemon
from .client_dockerhub import ClientHub
from .client_sw_service import ClientSoftware
import pika
import pika.exceptions
import logging
from .utils import get_logger


class Scanner:

    def __init__(self, versions_cmd="/resources/versions.yml", port_rabbit=5672, host_rabbit='172.17.0.2', url_imagesservice="http://127.0.0.1:8000/api/images"):

        self.logger = get_logger(__name__, logging.DEBUG)

        # client of software service
        self.client_software = ClientSoftware()

        # client for interacting with the docker daemon on the host
        self.client_daemon = ClientDaemon(base_url='unix://var/run/docker.sock')

        # RabbitQm connection
        self.parameters = pika.ConnectionParameters(host=host_rabbit, port=port_rabbit)
        # self.host_rabbit = host_rabbit
        # self.port_rabbit = port_rabbit

        # the clientApi talks with the server api in order to post the image description
        self.client_images = ClientImages(url_api=url_imagesservice)

        # the client hub interacts with the docker Hub registry
        self.client_hub = ClientHub()

    def run(self, rabbit_queue="dofinder"):
        try:
            self.logger.info("Connecting to " + self.parameters.host + ":" + str(self.parameters.port))
            connection = pika.BlockingConnection(self.parameters)
            channel = connection.channel()
        except pika.exceptions.ConnectionClosed as e:
            self.logger.exception("Connection Closed from rabbitMQ")
            return

        channel.queue_declare(queue=rabbit_queue, durable=True)  # make sure that the channel is created (e.g. if crawler start later)
        self.logger.info(" Waiting for messages. To exit press CTRL+C")

        def on_message(ch, method, properties, body):
            repo_name = body.decode()
            self.logger.info("Received " + repo_name)

            self.process_repo_name(repo_name)

            ch.basic_ack(delivery_tag=method.delivery_tag)   # ack to the server that the scanning is finished
            self.logger.debug("Sent ack to server for"+repo_name)

        # tell to rabbitMQ not to give moe than one message to a worker at a time
        # OR BETTER don't dispatch a new message to a worker until it has processed and acknowledged the previous one
        channel.basic_qos(prefetch_count=1)
        channel.basic_consume(on_message, queue=rabbit_queue)

        try:
            channel.start_consuming()
        except KeyboardInterrupt:
            channel.stop_consuming()
        channel.close()

    def process_repo_name(self, repo_name):
        if self.client_images.is_new(repo_name):       # the image is totally new
            dict_image = self.scan(repo_name)
            self.client_images.post_image(dict_image)  # POST the description of the image
            self.logger.info("[" + repo_name + "]  uploaded the image description")
        elif self.client_images.must_scanned(repo_name):  # the image must be scan again
            dict_image = self.scan(repo_name)
            self.client_images.put_image(dict_image)  # PUT the new image description of the image
            self.logger.info("[" + repo_name + "] updated the image description")
        else:
            self.logger.info("[" + repo_name + "] already up to date.")

    def scan(self, repo_name, tag="latest", rmi=False):

        try:
            self.client_daemon.pull_image(repo_name, tag)
        except:
            self.logger.exception("Exception when pulling the image")
            raise

        dict_image = {}
        self.logger.info('Scanning [{0}]'.format(repo_name))

        dict_image["repo_name"] = repo_name

        #self.info_inspect(repo_name, dict_image)
        self.info_docker_hub(repo_name, dict_image)
        self.info_dofinder(repo_name, dict_image)

        self.logger.info('Finish scanning [{0}]'.format(repo_name))
        dict_image['last_scan'] = str(datetime.datetime.now())
        if rmi:
            self.client_daemon.remove_image(repo_name, force=True)
        return dict_image

    # def info_inspect(self, repo_name, dict_image):
    #     """
    #      docker inspect IMAGE
    #     """
    #     self.logger.info'[{}] docker inspect ... '.format(repo_name))
    #     dict_inspect = self.client_daemon.inspect_image(repo_name)
    #     #dict_image['size'] = dict_inspect['Size']


    def info_docker_hub(self, repo_name, dict_image):
        """
        Download the image information among Docker API v2.
        :param repo_name:
        :param dict_image:
        :return:
        """
        self.logger.info('[{}] adding Docker Hub info ... '.format(repo_name))

        json_response = self.client_hub.get_json_repo(repo_name)

        if 'description' in json_response:
            dict_image['description'] = json_response['description']
        if 'star_count' in json_response:
            dict_image['star_count'] = json_response['star_count']
        if 'pull_count' in json_response:
            dict_image['pull_count'] = json_response['pull_count']


        # TODO : here must be included the tags lists of the image
        #josn_reposnse = slef.clientHub.get_all_tags(repo_name)

        # info of only the image with the tag latest
        json_response = self.client_hub.get_json_tag(repo_name, tag="latest")

        if 'last_updated' in json_response:
            dict_image['last_updated'] = json_response['last_updated']
        if 'full_size' in json_response:
            dict_image['full_size'] =json_response['full_size']

    def info_dofinder(self, repo_name, dict_image):

        self.logger.info('[{}] searching software ... '.format(repo_name))

        try:
            with Container(repo_name) as c:
                # search distribution
                for cmd, reg in self.client_software.get_system():# self._get_sys(self.versionCommands):
                    output = c.run(cmd)
                    p = re.compile(reg)
                    match = p.search(output)
                    if match:
                        # take the non-capturing group: only the matches, group[0] return all the match
                        dist = match.group(0)
                        dict_image['distro'] = dist
                    else:
                        self.logger.debug("[{0}] not found {1}".format(repo_name, cmd))

            with Container(repo_name) as c:
                # search binary versions
                bins = []
                for bin, cmd, regex in self.client_software.get_software():#elf._get_bins(self.versionCommands):
                    self.logger.debug("[{}] searching {} ".format(repo_name, bin))
                    output = c.run(bin+" "+cmd)
                    p = re.compile(regex)     # can be saved the compilatiion of the regex to savee time (if is equal to all the version)
                    match = p.search(output)
                    if match:
                        version = match.group(0)
                        self.logger.info("[{0}] found {1}: {2}".format(repo_name, bin, version))
                        bins.append({'bin': bin, 'ver': version})
                dict_image['bins'] = bins
        except docker.errors.APIError as e:
            self.logger.exception("Api Error")
    #
    # def _get_sys(self, yml_cmd):
    #     apps = yml_cmd['system']
    #     for app in apps:
    #         yield app["cmd"], app["re"]
    #
    # def _get_bins(self, yml_cmd):
    #     apps = yml_cmd['applications']
    #     for app in apps:
    #         yield app["name"], app["ver"], app["re"]

    def pull_officials(self):
        # TODO excpetion raise for the connection to docker hub
        # download all the official library
        images_libraries = self.client_hub.crawl_official_images()

        for image in images_libraries:
            try:
                self.logger.info("Pull official images ...")
                self.client_daemon.pull_image(image)
            except docker.errors.APIError:
                self.logger.exception("Docker api error")
                pass