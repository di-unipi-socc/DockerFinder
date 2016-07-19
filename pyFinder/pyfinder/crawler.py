import datetime
from . import utils
from .client_dockerhub import  ClientHub
import pika
import json
import pickle
import os
from . import constants


class Crawler:

    def __init__(self, port_rabbit=5672, host_rabbit='127.0.0.1', queue_rabbit="dofinder"):
        # self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=host_rabbit, port=port_rabbit))
        # self.channel = self.connection.channel()
        self.host_rabbit = host_rabbit
        self.port_rabbit = port_rabbit
        self.queue_rabbit = queue_rabbit
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.host_rabbit, port=self.port_rabbit))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=self.queue_rabbit, durable=True)

        self.client_hub = ClientHub()

    # def _connect_rabbit(self):
    #     self.connection = pika.BlockingConnection(
    #         pika.ConnectionParameters(host=self.host_rabbit, port=self.port_rabbit))
    #     self.channel = self.connection.channel()
    #     self.channel.queue_declare(queue=self.queue_rabbit, durable=True)

    def crawl(self,  from_page=1, page_size=10, max_images=100):
        print("[crawler] connecting to " + self.host_rabbit+":"+str(self.port_rabbit)+" queue:"+self.queue_rabbit+"...")

        # self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.host_rabbit, port=self.port_rabbit))
        # self.channel = self.connection.channel()
        # self.channel.queue_declare(queue=self.queue_rabbit, durable=True)

        print("Crawling the images from the docker Hub...")
        crawled_image, saved_images = 0, 0

        for list_images in self.client_hub.crawl_images(page=from_page, page_size=page_size, max_images=max_images):
            for image in list_images:
                crawled_image += 1
                list_tags = self.client_hub.get_all_tags(image['repo_name'])
                print("[ " + image['repo_name'] + " ] found tags " + str(len(list_tags)))
                #print(list_tags)
                if list_tags and 'latest' in list_tags:   # only the images that  contains "latest" tag
                    print("[" + image['repo_name'] + "] crawled from docker Hub")
                    saved_images += 1

                    # send into rabbitMQ server
                    self.send_to_rabbit(image['repo_name'])
                    print("[" + image['repo_name'] + "] sent to the rabbit channel")

            print("\n {0} numbers of images crawled : {1}".format("[crawler]", str(crawled_image)))
            print(" {0} number of images sent to queue: {1}\n".format("[crawler]", str(saved_images)))


        #close the connectino with rabbitMQ server
        self.connection.close()
        print("\n[crawler] closed connection of rabbitMq channel ")

    def send_to_rabbit(self, msg):
        #self.channel.queue_declare(queue=queue_rabbit, durable=True)
        self.channel.basic_publish(exchange='',
                                   routing_key=self.queue_rabbit,
                                   body=msg,
                                   properties=pika.BasicProperties(
                                            delivery_mode=2,       #make message persistent save the message to disk
                                    ))

    def build_test(self, num_images_test=100):
        list_image = self.get_test_image(num_images_test)
        for image in list_image:
            self.send_to_rabbit(image)

    def get_test_image(self, num_images_test=100):
        images_for_test = []
        for list_images in self.client_hub.crawl_images():
            for image in list_images:
                list_tags = self.client_hub.get_all_tags(image['repo_name'])
                if list_tags and 'latest' in list_tags and len(
                        images_for_test) < num_images_test:  # only the images that  contains "latest" tag
                    print("[" + image['repo_name'] + "] crawled from docker Hub")
                    images_for_test.append(image['repo_name'])
            if len(images_for_test) == num_images_test:
                self.dump_images(images_for_test)
                return images_for_test


    def dump_images(self, list_images):
        pickle.dump(list_images, open(os.path.dirname(__file__)+constants.FILE_NAME_IMAGES_TEST, "wb"))
        print("\n {0} number of  images for testing  in {1}".format("[crawler]",len(list_images), os.path.dirname(__file__)+constants.FILE_NAME_IMAGES_TEST))

    def load_test_images(self):
        list_images = pickle.load(open(os.path.dirname(__file__) + constants.FILE_NAME_IMAGES_TEST, "rb"))
        print("\n {0}  read  {1} images for testing  in {1}".format("[crawler]", len(list_images)))
        return list_images

    def run_test(self):
        list_images = self.load_test_images()

        for image in list_images:
            self.send_to_rabbit(image)
            print("\n {0} image sent to  {1}".format("[crawler]", len(self.queue_rabbit)))

        self.connection.close()