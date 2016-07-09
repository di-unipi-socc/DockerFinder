import datetime
from . import utils
from .client_dockerhub import  ClientHub
import pika
import json

class Crawler:

    def __init__(self, port=5672, rabbit_host='172.17.0.3'):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbit_host, port=port))
        self.channel = self.connection.channel()
        self.client_hub = ClientHub();


    def crawl(self, max_images=100, page_size=10, from_page=1):
        print("Crawling the images from the docker Hub...")
        crawled_image, saved_images = 0, 0
        for list_images in self.client_hub.crawl_images(page=from_page, page_size=page_size, max_images=max_images):
            for image in list_images:
                crawled_image += 1
                list_tags = self.client_hub.get_all_tags(image['repo_name'])
                print("[" + image['repo_name'] + "] found tags " + str(len(list_tags)))
                if list_tags and 'latest' in list_tags:   # only the images that  contains "latest" tag
                    print("[" + image['repo_name'] + "] crawled from docker Hub")
                    saved_images += 1

                    # send into rabbitMQ server
                    self.send_to_rabbit(image['repo_name'])#json.dumps(image, sort_keys=True, indent=4))
                    print("[" + image['repo_name'] + "] sent to the rabbit channel")

            print("\n {0} numbers of images crawled : {1}".format("[scanner]", str(crawled_image)))
            print(" {0} number of images sent to scanners: {1}\n".format("[scanner]", str(saved_images)))

        #close the connectino with rabbitMQ server
        self.connection.close()
        print("[scanner] closed connection of rabbitMq channel "+self.channel)

    def send_to_rabbit(self, msg, rabbit_queue="dofinder"):
        self.channel.queue_declare(queue=rabbit_queue, durable=True)
        self.channel.basic_publish(exchange='',
                                   routing_key=rabbit_queue,
                                   body=msg,
                                   properties=pika.BasicProperties(
                                            delivery_mode=2,       #make message persistent save the message to disk
                                    ))

