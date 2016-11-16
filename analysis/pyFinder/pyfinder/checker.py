from .client_images_service import ClientImages
from .client_dockerhub import ClientHub
from .publisher_rabbit import PublisherRabbit
from .utils import get_logger
import logging
import json
import pika
import time


class Checker:

    def __init__(self,  images_url="http://127.0.0.1:3000/api/images",
                        hub_url="https://hub.docker.com/",
                        amqp_url='amqp://guest:guest@127.0.0.1:5672',
                        exchange="dofinder",
                        queue="images",
                        route_key="images.scan",
                        ):

        # For publishing into RabbitMq queue the iamge name
        self.url_amqp = amqp_url
        self._exchange = exchange
        self._route_key =route_key

        #self.logger = get_logger(__name__, logging.INFO)
        self.logger = get_logger(__name__, logging.INFO)

        # client of Images Service:  in order to add and update the image description.
        self.client_images = ClientImages(images_url=images_url)

        # client of Docker Hub.
        self.client_hub = ClientHub(docker_hub_endpoint=hub_url)

    def send_to_rabbitmq(self, msg):
            connection = pika.BlockingConnection(pika.URLParameters(self.url_amqp))
            self.logger.info("connected to "+ self.url_amqp)
            # Open the channel
            channel = connection.channel()
            # Declare the queue
            self.logger.info(self._route_key)
            channel.basic_publish(exchange=self._exchange,
                      routing_key=self._route_key,
                      body=msg)

            self.logger.info(msg + " sent to "+self._exchange)
            # queue =  channel.queue_declare(queue=queue,
            #                 passive=True,
            #                 durable=True,
            #                 exclusive=False,
            #                 auto_delete=False
            #                 )
            # channel.basic_publish(e)

            connection.close()

    def check_images(self):
        checked = {}
        checked['removed'] = []
        checked['requeued'] = []
        #removed_images = 0
        #requeued_images = 0

        json_res = self.client_images.get_images()
        #json_res = {"count":<number>,"images":[..]}
        self.logger.info( str(json_res ['count']) + ": images prensent into local database")
        images = json_res['images']
        # { "name":<name:tag> }
        for image in images:
            self.logger.info( image['name'] + ": checking image")
            name = image['name']
            splitname = image['name'].split(":")
            repo = splitname[0]
            tag = splitname[1]
            image_id = image['_id']
            if not self.client_hub.is_alive_in_hub(repo, tag):
                self.client_images.delete_image(image_id)
                checked['removed'].append(name)
                #removed_images+=1
            else:
                if self.client_images.must_scanned(name):
                    self.logger.debug("["+name+"] out of date.")
                    self.send_to_rabbitmq(json.dumps({"name": repo }))
                    self.logger.info("["+name+"] requeued into queue.")
                    checked['requeued'].append(name)
                    #requeued_images+=1
        self.logger.info("Removed images: " + str(len(checked['removed']))+ "; Requeued images:"+ str(len(checked['requeued'])))

    def run(self, interval_next_check):
        self.logger.info("Starting the checker module...")
        while True:
            self.check_images()
            time.sleep(interval_next_check)
