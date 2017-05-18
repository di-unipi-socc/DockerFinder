import logging
import random
import json
import pickle
from pyfinder.core import ClientImages, PublisherRabbit, ClientHub


"""The module contains the source code of the *Crawler*."""


class Crawler:

    def __init__(self, exchange="dofinder",
                 queue="images",
                 route_key="images.scan",
                 amqp_url='amqp://guest:guest@127.0.0.1:5672',
                 images_url="http://127.0.0.1:3000/api/images",
                 hub_url="https://hub.docker.com",
                 path_last_url="/data/crawler/lasturl.txt",
                 policy="none",
                 min_stars=0,
                 min_pulls=0,
                 only_automated=False,
                 only_official=False
                 ):

        self.logger = logging.getLogger(__class__.__name__)
        self.logger.info(__class__.__name__ + " logger  initialized")

        # publish the images downloaded into the rabbitMQ server.
        self.publisher = PublisherRabbit(
            amqp_url, exchange=exchange, queue=queue, route_key=route_key)
        self.logger.info("RabbitMQ : exchange=" + exchange +
                         ", queue=" + queue + " route key=" + route_key)

        # Client of Docker Hub.
        self.client_hub = ClientHub(docker_hub_endpoint=hub_url,
                                    path_last_url=path_last_url)

        # client of Images Service:  if an image is NEW it is sent to queue,
        # otherwise it is discarded
        self.client_images = ClientImages(images_url=images_url)

        # ordering = {"stars":"star_count", "-stars":"-star_count",
        # "pulls":"pull_count", "-pulls":"-pull_count"}
        ordi = {"stars_first": "-star_count",
                "pulls_first": "-pull_count", "none": None}
        # {"stars_first":"-star_count", "pulls_first"  : "-pull_count",
        #  "none":None}.get(policy, None)
        self.ordering = ordi[policy]
        self.policy = policy

        self.min_stars = min_stars
        self.min_pulls = min_pulls
        self.only_automated = only_automated
        self.only_official = only_official
        self.logger.info("Crawler: ordering={}, policy={}, min_stars={}, min_pulls={}, only_official={}, only_automated={}".format(
            self.ordering, self.policy, min_stars, min_pulls, only_official, only_automated))

    # , max_images=None):
    def run(self, from_page, page_size, num_samples=None, at_random=False, force_from_page=False):
        """
        Starts the publisher of the RabbitMQ server, and send to the images crawled with the crawl() method.
        If num_sample != None:
            if at_random:
                crawls num_samples images using the random sampling method.
            else:
                crawl num_samples images in order
        else :
            crawls all the images from the Docker Hub.,

        :param from_page:  the starting page into the Docker Hub.
        :param page_size:  the number of images in a single page.
        :param max_images:  the number of images name to downloads.
        :return:
        """
        try:
            if num_samples != None:
                if at_random:
                    #self.publisher.run(images_generator_function=self.crawl(from_page=from_page, page_size=page_size, max_images=max_images))
                    self.publisher.run(images_generator_function=self.crawl_random_samples(
                        num_samples, force_from_page, from_page=from_page, page_size=page_size))  # , max_images=max_images))
                else:
                    self.publisher.run(images_generator_function=self.crawl(force_from_page=force_from_page,
                                                                            from_page=from_page, page_size=page_size, max_images=num_samples))  # , max_images=max_images))
            else:
                self.publisher.run(images_generator_function=self.crawl(
                    force_from_page=force_from_page, from_page=from_page, page_size=page_size, max_images=None))
        except KeyboardInterrupt:
            self.publisher.stop()

    def crawl_random_samples(self, m_samples, force_from_page, from_page, page_size):
        """
        This is a generator function that crawls docker images name at random name the Docker HUb.
        The following random sampling of a kNOWN STREAM is used.

            s = 0                //number of item selected
             for (j=1 ; j <= n; j++)
               p = Rand(0,1)
               if (p <= (m-s)/ n-j+1):
                  select S[j];
                  s++
        :param m_samples: number of sampled images,
        :param from_page:  the starting page into the Docker Hub.
        :param page_size:  is the number of images per image that Docker Hub return.
        :param max_images:  the number of images to download.
        :return: generator of JSON images description
        """

        # TODO : max_images and num_samples are different . Max _images tell to Docker Hub CLient the max number of images to be dowlodes
        # num_samples is the number of images to be sampled into Docker Hub.

        sent_images = 0
        max_images = None
        previous_num_sampled = 0  # only for logging the sampled images when the number cheange
        j = 0       # number of total imags passed thorugh the stream
        # total number of images stored within Docker Hub
        num_images = self.client_hub.count_all_images()
        # TODO: not all the images into the Dokcer Hub are downaloded if the
        # filter functioi is executed
        self.logger.info("Random sampling activated. \n\t\tTarget samples:" + str(m_samples) +
                         ", Total number of images: " + str(num_images) + "\n\t\tPercentage:" + str(m_samples / num_images))
        for list_images in self.client_hub.crawl_images(from_page=from_page,
                                                        page_size=page_size,
                                                        max_images=num_images,
                                                        force_from_page=force_from_page,
                                                        sort=self.ordering
                                                        ):
                                                        # filter_images=self.filter_tag_latest):
            previous_num_sampled = sent_images   # set the previous sent images
            for image in list_images:
                    # Random sampling over a stream of images
                j += 1
                # if j <= num_images : # otherwise division by zero
                p = random.uniform(0, 1)  # 0 <= p <= 1
                # if (p <= (m-s)/ n-j+1):
                if p <= (m_samples - sent_images) / (num_images - j + 1):
                    repo_name = image['repo_name']
                    sent_images += 1
                    yield json.dumps({"name": repo_name})
            if sent_images > previous_num_sampled:
                self.logger.info(
                    "{0}/{1} (Current samples/Target samples)".format(str(sent_images), str(m_samples)))

        self.logger.info("Total sampled images: {0}".format(str(sent_images)))

    def crawl(self, force_from_page, from_page, page_size, max_images=None):
        """
        The crawl() is a generator function. It crawls the docker images name from the Docker HUb.
        It yeld a  JSON of the image.
        :param from_page:  the starting page into the Docker Hub.
        :param page_size:  is the number of images per image that Docker Hub return.
        :param max_images:  the number of images to download.
        :return: generator of JSON images description
        """
        sent_images = 0
        #count = self.client_hub.count_all_images()
        #max_images = count if not max_images else max_images
        count = self.client_hub.count_all_images()
        if max_images is None:
            max_images = count
            self.logger.info("Consecutive sampling activated. \n\t\tTarget :" + str(max_images) +
                             ", Total images: " + str(count) + "\n\t\tPercentage:" + str(max_images / count))
        else:
            self.logger.info("Consecutive sampling activated. \n\t\tTarget :" + str(max_images) +
                             ". Total images: " + str(count) + "\n\t\tPercentage:" + str(max_images / count))
        for image in self.client_hub.crawl_images(from_page=from_page,
                                                  page_size=page_size,
                                                  max_images=max_images,
                                                  force_from_page=force_from_page,
                                                  sort=self.ordering,
                                                  # filter_image_tag=self.filter_tag
                                                  # filter_tag=self.filter_latest,
                                                  filter_repo=self.filter_tosker):
            sent_images += 1
            if sent_images % 100 == 0:
                self.logger.info(
                    "{0} number of images sent to analyser".format(sent_images))
            yield json.dumps(image)  # json.dumps({"name": repo_name})

            #self.logger.info("{0}/{1} (Current samples/Target samples)".format(str(sent_images), str(count)))
            #self.logger.info("Number of images sent to queue: {0}".format(str(sent_images)))
            #self.logger.info("{0}/{1} (Current samples/Target samples)".format(str(sent_images), str(count)))
        self.logger.info(
            "Total num of images sent to queue: {0}".format(sent_images))

    def filter_latest(self, image_with_tag):
        """
        Filters the images with the *latest* tag.
        An image is sento to the rabbitMQ only of it is new into the local database, otherwise it is
        discarded (The checker is in charge to requeue the images that are not updated)
        :param repo_name: the name of a repository
        :return: True if the image must be downloaded, Flase if must be discarded
        """
        process_image = False
        self.logger.debug(
            "[" + repo_name + "] filtering lates tag processing image.")

        return image_with_tag['tag'] == "latest"

    def filter_tosker(self, image):
        # self.logger.info(dir(self))

        # self.policy  = policy
        # self.min_stars =  min_stars
        # self.min_pulls =  min_pulls
        # self.only_automated =  only_automated
        # self.only_official  = only_official

        select_image = True
        stars = image['star_count']
        pulls = image['pull_count']
        is_automated = image['is_automated']
        is_official = image['is_official']

        # self.logger.info(self.only_automated)
        # self.logger.info(self.only_official)

        if stars < self.min_stars:
            #self.logger.info("stars {} {}"  .format(stars,self.min_stars )  )
            select_image = False
        if pulls < self.min_pulls:
            #self.logger.info("pulls {} {}"  .format(stars,self.min_stars )  )
            select_image = False
        if self.only_automated == True:
            if is_automated == False:
                self.logger.debug("not automated  ")
                select_image = False
        if self.only_official == True:
            if is_official == False:  # True:
                self.logger.debug("not official ")
                select_image = False
        return select_image
