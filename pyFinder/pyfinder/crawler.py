import json
import pickle
from .publisher_rabbit import PublisherRabbit
from .client_dockerhub import ClientHub
import logging
from .utils import get_logger


class Crawler:

    def __init__(self, exchange="dofinder",
                 queue="images",
                 route_key="images.scan",
                 amqp_url='amqp://guest:guest@127.0.0.1:5672',
                 hub_url="https://hub.docker.com/"
    ):
                 #port_rabbit=5672, host_rabbit='localhost', queue_rabbit="dofinder"):

        self.logger = get_logger(__name__, logging.DEBUG)

        # publish the images downloaded into the rabbitMQ server.
        self.publisher = PublisherRabbit(amqp_url, exchange=exchange, queue= queue, route_key=route_key)
        self.logger.info("Publisher rabbit initialized: exchange=" +exchange+", queue="+queue+" route key="+route_key)

        # Client hub in order to get the images
        self.client_hub = ClientHub(docker_hub_endpoint=hub_url)

    def run(self, from_page=1, page_size=10, max_images=100):
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

    def crawl(self, from_page=1, page_size=10, max_images=100):
        """
        The crawl() is a generator function. It crawls the docker images name from the Docker HUb.
        IT return a JSON of the image .
        :param from_page:  the starting page into the Docker Hub.
        :param page_size:  is the number of images per image that Docker Hub return.
        :param max_images:  the number of images  name to downloads.
        :return:  generator of JSON images description
        """

        self.logger.info("Crawling the images from the docker Hub...")
        crawled_image, saved_images = 0, 0
        for list_images in self.client_hub.crawl_images(page=from_page, page_size=page_size, max_images=max_images):
            for image in list_images:
                crawled_image += 1
                self.filter_image()
                list_tags = self.client_hub.get_all_tags(image['repo_name'])
                self.logger.debug(" [ " + image['repo_name'] + " ] found tags " + str(len(list_tags)))
                #print(list_tags)
                if list_tags and 'latest' in list_tags:   # only the images that  contains "latest" tag
                    self.logger.debug(" [" + image['repo_name'] + "] crawled from docker Hub")
                    saved_images += 1
                    info_image = dict()
                    info_image['name'] = image['repo_name']
                    yield json.dumps(info_image)

            self.logger.info("Numbers of images crawled : {0}".format(str(crawled_image)))
            self.logger.info("Number of images sent to queue: {0}\n".format(str(saved_images)))

    def generator_test_images(self, path_name_file):
        list_images=[]
        try:
            with open(path_name_file, "rb") as f:
                self.logger.info("Read  {1} images for testing in file".format(len(list_images), path_name_file))
                list_images = pickle.load(f)
                for image in list_images:
                    yield json.dumps({"name":image})

        except FileNotFoundError:
            self.logger.exception(" Error open file "+path_name_file+". Try [ build test ] command")
            raise
        except Exception:
            self.logger.exception("unexpected Exception")
            raise
        #return list_images

    def run_test(self, path_name_file="images.test"):
        self.generator_test_images(path_name_file)

        try:
            self.publisher.run(
                images_generator_function=self.generator_test_images(path_name_file))
        except KeyboardInterrupt:
            self.publisher.stop()

