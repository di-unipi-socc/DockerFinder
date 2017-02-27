from pyfinder.core import ClientImages, PublisherRabbit, ClientHub

import logging
from logging.handlers import TimedRotatingFileHandler
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
                        path_file_logging=None
                        ):



        # For publishing into RabbitMq queue the iamge name
        self.url_amqp = amqp_url
        self._exchange = exchange
        self._route_key =route_key

        # stream handler logger

        self.logger = logging.getLogger(__class__.__name__)
        self.logger.info(__class__.__name__ + " logger  initialized")

        # file handler logger
        self.path_file_logging = path_file_logging
        self.file_logger = None
        if path_file_logging:
            name_file_logger = __class__.__name__+"-rotated"
            self.file_logger = logging.getLogger(name_file_logger)

            self.file_logger.setLevel(logging.DEBUG)

            interval = 24
            backupCount = 10  # 10 giorni di backup
            self.logger.info("LOGGING PATH: "+path_file_logging + " every hour="+ str(interval)+" with backupcount="+str(backupCount))

            handler = TimedRotatingFileHandler(path_file_logging,
                                       when="h",
                                       interval=interval,
                                       backupCount=backupCount)

            #fh = logging.FileHandler(path_file_logging)
            #fh.setLevel(logging.DEBUG)
            LOG_FORMAT = ('%(asctime)s %(message)s')
            formatter = logging.Formatter(LOG_FORMAT)
            #fh.setFormatter(formatter)
            # add the file handlers handlers to the logger
            #self.file_logger.addHandler(fh)
            handler.setLevel(logging.INFO)
            handler.setFormatter(formatter)
            self.file_logger.addHandler(handler)
            #str(tot_hub_images)+":"+str(tot_dockerfinder_images)+":"+ str(removed)+":"+str(pending)+":"+str(uptodate)
            self.file_logger.info("hubtot:dftot:dfremoved:dfpending:dfuptodate")

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

            connection.close()

    def check_images(self):
        """
        scan the images.
        """
        checked = {}
        tot_dockerfinder_images = 0
        removed = 0
        pending = 0
        uptodate = 0

        json_res = self.client_images.get_images()
        tot_dockerfinder_images = json_res ['count']
        self.logger.info(str(tot_dockerfinder_images) + " images present into local database")
        tot_hub_images = self.client_hub.count_all_images()
        self.logger.info(str(tot_hub_images) + ": images present into Docker Hub")
        images = json_res['images']
        for image in images:
            name = image['name']
            splitname = image['name'].split(":")
            repo = splitname[0]
            tag = splitname[1]
            image_id = image['_id']
            if self.client_hub.is_alive_in_hub(repo, tag):
                self.logger.debug("["+name+"]status:" +image['status'])
                if image['status'] == "updated":
                    #self.logger.info("["+name+"] status UPDTED")
                    if self.client_images.must_scanned(name):
                        self.logger.debug("["+name+"] must be scanned again.")
                        self.client_images.update_status(image_id, "pending")  # Set status to Pending
                        self.logger.info("["+name+"] from UPDATED to PENDING status.")
                        self.send_to_rabbitmq(json.dumps({"name": repo }))
                        self.logger.info("["+name+"] requeud into queue.")
                        #checked['pending'].append(name)
                        pending +=1
                    else:
                        self.logger.info("["+name+"] remains UPDATED status.")
                        uptodate +=1
                if image['status'] == "pending":
                    self.logger.debug("["+name+"] remains PENDING status")
                    pending +=1
            else:
                #the image is removed from the database if it is not present into Docker Hub
                self.client_images.delete_image(image_id)
                removed += 1
        if  self.path_file_logging:
            self.file_logger.info(str(tot_hub_images)+":"+str(tot_dockerfinder_images)+":"+
                            str(removed)+":"+str(pending)+":"+str(uptodate))
        assert tot_dockerfinder_images == (pending+uptodate+removed)
        self.logger.info("Removed=" + str(removed)+ "; pending="+ str(pending)+ " up-to-date="+str(uptodate))

    def verify_images(self):
        """
        Scan all the images in the local databse and fix the problems
           1) having the ".go" or "." version of a software.
           2) is_private = null,
           3) is_automated = nul
        by updating the boolean value from Doker Hub.

        """

        json_res = self.client_images.get_images()
        tot_dockerfinder_images = json_res ['count']
        self.logger.info(str(tot_dockerfinder_images) + " images present into local database")
        images = json_res['images']
        updated = 0
        for image in images:
            name  =  image['name']
            splitname = image['name'].split(":")
            repo = splitname[0]
            tag = splitname[1]
            json_response = self.client_hub.get_json_repo(repo)
            if json_response:
                if "is_automated" in json_response:
                    image['is_automated'] =  json_response['is_automated']

                if "is_private" in json_response:
                    image['is_private']  =  json_response['is_private']
                softwares =   image['softwares']
                self.logger.info("before: {0}".format(softwares))
                # [0-9]+[.][0-9]*[.0-9]

                softwares = [sw for sw in softwares if sw['ver'] != '.']
                softwares = [sw for sw in softwares if sw['ver'] != ".go"]
                #for sw in softwares:
                #    if ".go" in sw['ver'] or sw['ver'] == ".":
                #        self.logger.info("removing {0}:{1}".format(sw['software'], sw['ver']))
                #        softwares.remove(sw)
                self.logger.info("after: {0}".format(softwares))
                image['softwares']  = softwares

            self.client_images.put_image(image)  # PUT the new image description of the image
            updated += 1
            self.logger.info("UPDATED ["+name+"]. {0}/{1}".format(updated, tot_dockerfinder_images) )

    def run(self, interval_next_check):
        self.logger.info("Starting the checker module...")
        while True:
            try:
                self.check_images()
                time.sleep(interval_next_check)
            except  Exception as e:
                self.logger.error(str(e))
                self.logger.error("Waiting 5s and restarting.")
                time.sleep(5)
