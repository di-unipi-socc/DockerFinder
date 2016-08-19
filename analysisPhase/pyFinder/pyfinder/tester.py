import pickle
from .client_dockerhub import ClientHub
from .utils import get_logger
import logging

logger = get_logger(__name__, logging.INFO)

def get_test_image(num_images_test=100):
    images_for_test = []
    client_hub = ClientHub()
    for list_images in client_hub.crawl_images():
        for image in list_images:
            list_tags = client_hub.get_all_tags(image['repo_name'])
            if list_tags and 'latest' in list_tags and len(images_for_test) < num_images_test:  # only the images that  contains "latest" tag
                images_for_test.append(image['repo_name'])
                logger.info("[" + image['repo_name'] + "] crawled from docker Hub")
        if len(images_for_test) == num_images_test:
            return images_for_test


def build_test(path_name_file="images.test", num_images_test=100):
    list_images_test = get_test_image(num_images_test)
    dump_test_images(list_images_test, path_name_file)


def dump_test_images(list_images, path_name):
    with open(path_name, "wb") as f:
        pickle.dump(list_images, f)
    logger.info(" Saved {0} images for testing in {1}".format(len(list_images), path_name))