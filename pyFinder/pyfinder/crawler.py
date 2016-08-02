import datetime
from . import utils
from .client_dockerhub import  ClientHub
import pika
import pika.exceptions as e
import json
import pickle
import os
import logging
from .utils import get_logger


class Crawler:

    def __init__(self, port_rabbit=5672, host_rabbit='localhost', queue_rabbit="dofinder"):

        self.logger = get_logger(__name__, logging.DEBUG)
        self.host_rabbit = host_rabbit
        self.port_rabbit = port_rabbit
        self.queue_rabbit = queue_rabbit

        self.parameters = pika.ConnectionParameters(
            host=host_rabbit,
            port=port_rabbit,
            heartbeat_interval=30,   # how often send heartbit (default is None)
            connection_attempts=3,
            retry_delay=3,           # time in seconds
        )
        self.logger.debug("Connection  parameters rabbit:"+ \
                          " Heartbeat: "+str(self.parameters.heartbeat) + \
                          " Connection_attemps: "+str(self.parameters.connection_attempts)+\
                          " Retry delay: "+ str(self.parameters.retry_delay))
        try:
            self.logger.info("Connecting to "+self.parameters.host+":"+str(self.parameters.port))
            self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.host_rabbit, port=self.port_rabbit))
        except e.ConnectionClosed:
            self.logger.error("Fail connecting to "+self.parameters.host+":"+str(self.parameters.port))
            raise

        self.channel = self.connection.channel()
        self.logger.info("Connecting to queue:"+self.queue_rabbit)
        self.channel.queue_declare(queue=self.queue_rabbit, durable=True)

        # Client hub in order to get the images
        self.client_hub = ClientHub()

    def crawl(self,  from_page=1, page_size=10, max_images=100):
        #self.logger.info(" Connecting to " + self.host_rabbit+":"+str(self.port_rabbit)+" queue:"+self.queue_rabbit+ "...")
        #print("[crawler] connecting to " + self.host_rabbit+":"+str(self.port_rabbit)+" queue:"+self.queue_rabbit+"...")

        # self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.host_rabbit, port=self.port_rabbit))
        # self.channel = self.connection.channel()
        # self.channel.queue_declare(queue=self.queue_rabbit, durable=True)

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
                    msg = image['repo_name']
                    self.send_to_rabbit(msg)
                    self.logger.info("[" + msg + "] sent to the queue "+self.queue_rabbit)

            self.logger.info("Numbers of images crawled : {0}".format(str(crawled_image)))
            self.logger.info("Number of images sent to queue: {0}\n".format(str(saved_images)))

        self.connection.close()
        self.logger.debug("Closed connection")

    def send_to_rabbit(self, msg):
        self.channel.basic_publish(exchange='',
                                   routing_key=self.queue_rabbit,
                                   body=msg,
                                   properties=pika.BasicProperties(
                                            delivery_mode=2,       #make message persistent save the message to disk
                                    ))

    def load_test_images(self, path_name_file):
        list_images=[]
        try:
            with open(path_name_file, "rb") as f:
                list_images = pickle.load(f)
        except FileNotFoundError:
            self.logger.exception(" Error open file "+path_name_file+". Try [ build test ] command")
            raise
        except Exception:
            self.logger.exception("unexpected Exception")
            raise

        self.logger.info("Read  {1} images for testing in file".format(len(list_images),path_name_file))
        return list_images

    def run_test(self, path_name_file="images.test"):
        list_images = self.load_test_images(path_name_file)

        for image in list_images:
            self.send_to_rabbit(image)
            self.logger.info("["+image+"] sent to channel queue"+self.queue_rabbit)

        self.connection.close()
        self.logger.info("Connection closed")