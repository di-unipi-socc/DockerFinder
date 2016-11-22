import pickle
from .crawler import Crawler
from .client_dockerhub import ClientHub
from .publisher_rabbit import PublisherRabbit
import logging
import docker
import json
import time


"""This module contains the methods for executing the tests of the architecture. """

class Tester:
    def __init__(self, path_file_images="images.test",  hub_url="https://hub.docker.com/"):
        self._path = path_file_images
        self.crawler = Crawler()
        self.logger = logging.getLogger(__class__.__name__)
        self.logger.info(__class__.__name__ + " logger  initialized")
        # the client hub interacts with the docker Hub registry
        self.client_hub = ClientHub(docker_hub_endpoint=hub_url)
        self.client_daemon = docker.Client(base_url='unix://var/run/docker.sock')

    def build_test(self, num_images_test=100, from_page=1, page_size=10,):
        list_json_images = [image_json for image_json in self.crawler.crawl(max_images=num_images_test, from_page=from_page, page_size=page_size)]
        self.dump_test_images(list_json_images)

    def dump_test_images(self, list_images):
        with open(self._path, "wb") as f:
            pickle.dump(list_images, f)
            self.logger.info("Saved {0} images for testing in {1}".format(len(list_images), self._path))

    def push_test(self, amqp_url="amqp://guest:guest@180.0.0.3:5672", exchange="dofinder", queue="test", route_key="images.test"):
        publisher = PublisherRabbit(amqp_url, exchange=exchange, queue=queue, route_key=route_key)
        publisher.run(images_generator_function=self.generator_images_test())

    def generator_images_test(self):
        try:
            with open(self._path, "rb") as f:
                list_images = pickle.load(f)
                self.logger.info("Read  {1} images for testing in file".format(len(list_images), self._path))
                for image in list_images:
                    yield json.dumps(json.loads(image))
        except FileNotFoundError:
            logger.exception(" Error open file " + path_name_file + ". \n Try [ build test ] command before")
            raise
        except Exception:
            logger.exception("unexpected Exception")
            raise

    def pull_officials(self):
        # TODO excpetion raise for the connection to docker hub
        # download all the official library
        images_libraries = self.client_hub.crawl_official_images()
        self.logger.info("[" + str(len(images_libraries)) + "] number of official images to pull...")
        for image in images_libraries:
            try:
                self.client_daemon.pull(image)
            except docker.errors.APIError:
                self.logger.exception("Docker api error")


    def remove_no_officials(self):
        images_libraries = self.client_hub.crawl_official_images()
        all_images = self.client_daemon.images()

        for image in all_images:
            image_tags = image['RepoTags']
            for repo_tag in image_tags:   #repo_tag = "repo_name:latest"
                name = repo_tag.split(":")[0]
                if name not in images_libraries:
                    self.logger.info("Removing  " + repo_tag)
                    self.client_daemon.remove_image(repo_tag, force=True)
