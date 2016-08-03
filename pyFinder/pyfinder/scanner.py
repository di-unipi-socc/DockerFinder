import docker
import docker.errors
import re
from .container import Container
from .utils import *
from .client_images_service import ClientImages
from .client_daemon import ClientDaemon
from .client_dockerhub import ClientHub
from .client_software import ClientSoftware
from .consumer_rabbit import ConsumerRabbit
from .utils import get_logger
import logging


class Scanner:
    def __init__(self, amqp_url='amqp://guest:guest@180.0.0.4:5672', exchange=None, queue=None, route_key=None,
                 software_url="http://127.0.0.1:3001/api/software",
                 images_url="http://127.0.0.1:3000/api/iames",
                 hub_url="https://hub.docker.com/",
                 rmi=True):

        self.rmi = rmi  # remove an image ofter the scan

        self.logger = get_logger(__name__, logging.DEBUG)

        # client of software service: the service that return the software to search in the images.
        self.client_software = ClientSoftware(api_url=software_url)

        # client for interacting with the docker daemon on the host
        self.client_daemon = ClientDaemon(base_url='unix://var/run/docker.sock')

        # rabbit consumer for receiving the images, on_message_callback is called when a message is received
        self.consumer = ConsumerRabbit(amqp_url=amqp_url,
                                       exchange=exchange,
                                       queue=queue,
                                       route_key=route_key,
                                       on_msg_callback=self.on_message)

        # the clientApi interacts with the server api in order to post the image description
        self.client_images = ClientImages(images_url=images_url)
        # host_service=host_images, port_service=port_images, url_path=path_images)

        # the client hub interacts with the docker Hub registry
        self.client_hub = ClientHub(docker_hub_endpoint=hub_url)

    def on_message(self, json_message):
        """
        This is the callback function that is called when the consumer Rabbit receives a message.
        """
        self.logger.info("Received message:" + str(json_message))
        self.process_repo_name(json_message['name'])

    def run(self):
        try:
            self.consumer.run()
        except KeyboardInterrupt:
            self.consumer.stop()

    def process_repo_name(self, repo_name):
        self.logger.info("["+repo_name+"] Processing image")
        if self.client_images.is_new(repo_name):  # the image is totally new
            self.logger.debug("[" + repo_name + "] is totally new into the images server")
            dict_image = self.scan(repo_name)
            self.client_images.post_image(dict_image)  # POST the description of the image
            self.logger.info("[" + repo_name + "]  uploaded the new image description")
        elif self.client_images.must_scanned(repo_name):  # the image must be scan again
            self.logger.debug("[" + repo_name + "] is present into images server but must be scan again")
            dict_image = self.scan(repo_name)
            self.client_images.put_image(dict_image)  # PUT the new image description of the image
            self.logger.info("[" + repo_name + "] updated the image description")
        else:
            self.logger.info("[" + repo_name + "] already up to date.")

    def scan(self, repo_name, tag="latest"):
        try:
            self.client_daemon.pull_image(repo_name, tag)
        except:
            self.logger.exception("Exception when pulling the image")
            raise

        dict_image = {}
        self.logger.info('Scanning [{0}]'.format(repo_name))

        dict_image["repo_name"] = repo_name

        # self.info_inspect(repo_name, dict_image)
        self.info_docker_hub(repo_name, dict_image)

        self.info_dofinder(repo_name, dict_image)

        self.logger.info('Finish scanning [{0}]'.format(repo_name))
        dict_image['last_scan'] = str(datetime.datetime.now())

        if self.rmi:
            self.client_daemon.remove_image(repo_name, force=True)
            self.logger.info('[{0}] removed image'.format(repo_name))
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
        # josn_reposnse = slef.clientHub.get_all_tags(repo_name)

        # info of only the image with the tag latest
        json_response = self.client_hub.get_json_tag(repo_name, tag="latest")

        if 'last_updated' in json_response:
            dict_image['last_updated'] = json_response['last_updated']
        if 'full_size' in json_response:
            dict_image['full_size'] = json_response['full_size']

    def info_dofinder(self, repo_name, dict_image):

        self.logger.info('[{}] searching software ... '.format(repo_name))

        try:
            with Container(repo_name) as c:
                # search distribution
                for cmd, reg in self.client_software.get_system():  # self._get_sys(self.versionCommands):
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
                for software in self.client_software.get_software():  # self._get_bins(self.versionCommands):
                    bin = software['name']
                    cmd = software['cmd']
                    regex = software['regex']
                    # bin, cmd, regex
                    self.logger.debug("[{}] searching {} ".format(repo_name, bin))
                    output = c.run(bin + " " + cmd)
                    p = re.compile(
                        regex)  # can be saved the compilatiion of the regex to save time (if is equal to all the version)
                    match = p.search(output)
                    if match:
                        version = match.group(0)
                        self.logger.debug("[{0}] found {1}: {2}".format(repo_name, bin, version))
                        bins.append({'bin': bin, 'ver': version})
                dict_image['bins'] = bins
        except docker.errors.APIError as e:
            self.logger.exception("Api Error")
            raise

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
