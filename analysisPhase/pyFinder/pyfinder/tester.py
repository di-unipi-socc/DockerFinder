import pickle
from .crawler import Crawler
from .utils import get_logger
from .publisher_rabbit import PublisherRabbit
import logging
import json



#c = Crawler()
# def get_test_image(num_images_test=100):
#     images_for_test = []
#     client_hub = ClientHub()
#     for list_images in client_hub.crawl_images():
#         for image in list_images:
#             list_tags = client_hub.get_all_tags(image['repo_name'])
#             if list_tags and 'latest' in list_tags and len(images_for_test) < num_images_test:  # only the images that  contains "latest" tag
#                 images_for_test.append(image['repo_name'])
#                 logger.info("[" + image['repo_name'] + "] crawled from docker Hub")
#         if len(images_for_test) == num_images_test:
#             return images_for_test


class Tester:
    def __init__(self, path_file_images="images.test"):
        self._path = path_file_images
        self.crawler = Crawler()
        self.logger = get_logger(__name__, logging.INFO)

    def build_test(self, num_images_test=100, from_page=1, page_size=10,):
        list_json_images = [image_json for image_json in self.crawler.crawl(max_images=num_images_test, from_page=from_page, page_size=page_size)]
        self.dump_test_images(list_json_images)

    def dump_test_images(self, list_images):
        with open(self._path, "wb") as f:
            pickle.dump(list_images, f)
            self.logger.info("Saved {0} images for testing in {1}".format(len(list_images), self._path))

    def push_test(self,amqp_url="amqp://guest:guest@180.0.0.3:5672",exchange="dofinder",queue="test",route_key="images.test"):
        publisher = PublisherRabbit(amqp_url, exchange=exchange, queue=queue, route_key=route_key)
        publisher.run(images_generator_function=self.generator_images_test())

    def generator_images_test(self):
        try:
            with open(self._path, "rb") as f:
                list_images = pickle.load(f)
                self.logger.info("Read  {1} images for testing in file".format(len(list_images), self._path))
                for image in list_images:
                    yield str(json.loads(image))
        except FileNotFoundError:
            logger.exception(" Error open file " + path_name_file + ". Try [ build test ] command before")
            raise
        except Exception:
            logger.exception("unexpected Exception")
            raise
