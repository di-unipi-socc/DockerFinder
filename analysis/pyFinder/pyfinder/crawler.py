import json
import pickle
from .publisher_rabbit import PublisherRabbit
from .client_images_service import ClientImages
from .client_dockerhub import ClientHub
import logging
from .utils import get_logger

"""The module contains the *Crawler* implementation."""


class Crawler:

    def __init__(self, exchange="dofinder",
                 queue="images",
                 route_key="images.scan",
                 amqp_url='amqp://guest:guest@127.0.0.1:5672',
                 images_url="http://127.0.0.1:3000/api/images",
                 hub_url="https://hub.docker.com",
                 path_last_url="/data/crawler/lasturl.txt"
                ):

        self.logger = get_logger(__name__, logging.INFO)

        # publish the images downloaded into the rabbitMQ server.
        self.publisher = PublisherRabbit(amqp_url, exchange=exchange, queue= queue, route_key=route_key)
        self.logger.info("RabbitMQ : exchange=" +exchange+", queue="+queue+" route key="+route_key)

        # Client of Docker Hub.
        self.client_hub = ClientHub(docker_hub_endpoint=hub_url, path_last_url=path_last_url)

        # client of Images Service:  in order to add and update the image description.
        self.client_images = ClientImages(images_url=images_url)

    def run(self, from_page, page_size, max_images=100):
        """
        Starts the publisher of the RabbitMQ server, and send to the images crawled with the crawl() method.
        :param from_page:  the starting page into the Docker Hub.
        :param page_size:  is the number of images per image that Docker Hub return.
        :param max_images:  the number of images  name to downloads.
        :return:
        """
        try:
            self.publisher.run(images_generator_function=self.crawl(from_page=from_page, page_size=page_size, max_images=max_images))
        except KeyboardInterrupt:
            self.publisher.stop()
    def crawl(self, from_page, page_size, max_images=None):
        """
        The crawl() is a generator function. It crawls the docker images name from the Docker HUb.
        IT return a JSON of the image .
        :param from_page:  the starting page into the Docker Hub.
        :param page_size:  is the number of images per image that Docker Hub return.
        :param max_images:  the number of images to download.
        :return: generator of JSON images description
        """

        #self.logger.info("Crawling the images from the docker Hub...")
        sent_images = 0

        for list_images in self.client_hub.crawl_images(from_page=from_page,
                                                        page_size=page_size,
                                                        max_images=max_images,
                                                        filter_images=self.filter_tag_latest):

            for image in list_images:
                repo_name = image['repo_name']
                sent_images += 1
                yield json.dumps({"name": repo_name})
            self.logger.info("Number of images sent to queue: {0}".format(str(sent_images)))
        self.logger.info("Number of images sent to queue: {0}".format(str(sent_images)))


    def filter_tag_latest(self, repo_name):
        """
        Filters the images with the *latest* tag.
        :param repo_name: the name of a repository
        :return: True if the image must be downloaded, Flase if must be discarded
        """
        process_image = False
        self.logger.debug("[" + repo_name + "] processing image.")
        list_tags = self.client_hub.get_all_tags(repo_name)
        #self.logger.info(str(list_tags))
        if list_tags and 'latest' in list_tags:
            json_image_latest = self.client_hub.get_json_tag(repo_name, tag='latest')
            size  =  json_image_latest['full_size']
            if size and size > 0:
                if self.client_images.is_new(repo_name):  # the image is totally new
                    self.logger.debug("[" + repo_name + "]  is new into local database")
                    process_image = True
                    self.logger.debug("[" + repo_name + "] selected")
                else:
                    self.logger.debug("[" + repo_name + "] already present into local database.")
                    process_image = False
                    self.logger.debug("[" + repo_name + "] NOT selected")
            else:
                process_image = False
                self.logger.debug("[" + repo_name + "] not selected")
        return process_image
