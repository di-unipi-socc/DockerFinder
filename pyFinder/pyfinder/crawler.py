import datetime
from . import utils
from .client_dockerhub import  ClientHub
import pika
import pika.exceptions as e
import json
import pickle
import os
import logging
from . import constants
from .utils import get_logger


class Crawler:

    def __init__(self, port_rabbit=5672, host_rabbit='127.0.0.1', queue_rabbit="dofinder"):

        self.logger = get_logger(__name__, logging.INFO)
        self.host_rabbit = host_rabbit
        self.port_rabbit = port_rabbit
        self.queue_rabbit = queue_rabbit
        try:
            self.logger.info("Connecting to "+host_rabbit+":"+str(port_rabbit)+" queue: "+queue_rabbit)
            self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.host_rabbit, port=self.port_rabbit))
        except e.ConnectionClosed:
            self.logger.error("Fail connecting to rabbit server")
            raise

        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=self.queue_rabbit, durable=True)


        self.client_hub = ClientHub()



    # def _connect_rabbit(self):
    #     self.connection = pika.BlockingConnection(
    #         pika.ConnectionParameters(host=self.host_rabbit, port=self.port_rabbit))
    #     self.channel = self.connection.channel()
    #     self.channel.queue_declare(queue=self.queue_rabbit, durable=True)

    def crawl(self,  from_page=1, page_size=10, max_images=100):
        #self.logger.info(" Connecting to " + self.host_rabbit+":"+str(self.port_rabbit)+" queue:"+self.queue_rabbit+ "...")
        #print("[crawler] connecting to " + self.host_rabbit+":"+str(self.port_rabbit)+" queue:"+self.queue_rabbit+"...")

        # self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.host_rabbit, port=self.port_rabbit))
        # self.channel = self.connection.channel()
        # self.channel.queue_declare(queue=self.queue_rabbit, durable=True)

        #print("Crawling the images from the docker Hub...")
        self.logger.info("Crawling the images from the docker Hub...")
        crawled_image, saved_images = 0, 0
        for list_images in self.client_hub.crawl_images(page=from_page, page_size=page_size, max_images=max_images):
            for image in list_images:
                crawled_image += 1
                list_tags = self.client_hub.get_all_tags(image['repo_name'])
                self.logger.debug(" [ " + image['repo_name'] + " ] found tags " + str(len(list_tags)))
                #print(list_tags)
                if list_tags and 'latest' in list_tags:   # only the images that  contains "latest" tag
                    self.logger.debug(" [" + image['repo_name'] + "] crawled from docker Hub")
                    saved_images += 1

                    # send into rabbitMQ server
                    self.send_to_rabbit(image['repo_name'])
                    self.logger.info("[" + image['repo_name'] + "] sent to the queue "+self.queue_rabbit)

            self.logger.info("Numbers of images crawled : {0}".format(str(crawled_image)))
            self.logger.info("Number of images sent to queue: {0}\n".format(str(saved_images)))

        self.connection.close()
        #print("\n[crawler] closed connection of rabbitMq channel ")

    def send_to_rabbit(self, msg):
        self.channel.basic_publish(exchange='',
                                   routing_key=self.queue_rabbit,
                                   body=msg,
                                   properties=pika.BasicProperties(
                                            delivery_mode=2,       #make message persistent save the message to disk
                                    ))
        self.logger.info("[" + msg + "] sent to queue: " + self.queue_rabbit)



    def get_test_image(self, num_images_test=100):
        images_for_test = []
        for list_images in self.client_hub.crawl_images():
            for image in list_images:
                list_tags = self.client_hub.get_all_tags(image['repo_name'])
                if list_tags and 'latest' in list_tags and len(
                        images_for_test) < num_images_test:  # only the images that  contains "latest" tag
                    images_for_test.append(image['repo_name'])
                    self.logger.debug("[" + image['repo_name'] + "] crawled from docker Hub")
            if len(images_for_test) == num_images_test:
                self.dump_test_images(images_for_test)
                return images_for_test

    def dump_test_images(self, list_images, path_name):
        #pickle.dump(list_images, open(os.path.dirname(__file__)+constants.FILE_NAME_IMAGES_TEST, "wb"))
        pickle.dump(list_images, open(path_name, "wb"))
        self.logger.debug(" Saved {1} images for testing in {1}".format(len(list_images), path_name))

    def load_test_images(self, path_name_file):
        #list_images = pickle.load(open(os.path.dirname(__file__) + constants.FILE_NAME_IMAGES_TEST, "rb"))
        list_images = pickle.load(open(path_name_file, "rb"))
        self.logger.debug("Read  {1} images for testing ".format(len(list_images)))
        return list_images

    def build_test(self, path_name_file="images.test", num_images_test=100):
        list_images_test = self.get_test_image(num_images_test)
        self.dump_test_images(list_images_test, path_name_file)
        # for image in list_image:
        #    self.send_to_rabbit(image)

    def run_test(self, path_name_file="images.test"):
        list_images = self.load_test_images(path_name_file)

        for image in list_images:
            self.send_to_rabbit(image)

        self.connection.close()