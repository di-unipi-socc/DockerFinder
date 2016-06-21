import urllib.request
import json
import datetime
from mongoengine import *
from .model.hub import Hub
from .utils import *


class Crawler:

    def __init__(self, alias_db, host='localhost', port=27017):

        self.host = host
        self.alias_db = alias_db
        connect(alias_db, host=host, port=port)

    def crawl(self):
        i = 1
        next = ""
        print("Crawling the images from the docker Hub...")
        crawled_image, saved_images = 0, 0
        while next is not None:# and i != 5:
            url = self.build_search_url(i, 100)
            json_response = req_to_json(url)
            hub_images = json_response['results']   # 'results' is a list of images
            crawled_image += len(hub_images)
            image_to_save = []
            for im in hub_images:
                hub_image = self.extract_info(im)   # Hub image model
                list_tags = get_all_tags(im['repo_name'])
                if len(list_tags) > 0 and 'latest' in list_tags:   # if contains latest tag will be dowloaded
                    hub_image = self.extract_info(im)
                    hub_image.tags = list_tags
                    #print("[" + im['repo_name'] + "] crawled from docker Hub")
                    image_to_save.append(hub_image)
            if len(image_to_save) > 0:
                self.save_into_db(image_to_save)
                saved_images += len(image_to_save)
            next = json_response['next']
            i += 1
            print("\n {0} Crawled images ".format(str(crawled_image)))
            print(" {0} Saved images \n".format(str(saved_images)))

    def get_crawled_images(self):
        return Hub.objects


    def extract_info(self, image):

        repo_name = image['repo_name']

        hub_info = Hub(repo_name=repo_name)
        hub_info.pull_count = image['pull_count']
        hub_info.star_count = image['star_count']
        hub_info.is_official = image['is_official']
        hub_info.is_automated = image['is_automated']
        hub_info.short_description = image['short_description']
        hub_info.repo_owner = image['repo_owner']
        hub_info.t_crawl = datetime.datetime.now

        return hub_info

    def build_search_url(self, page_n, page_size=10):
        #https: // hub.docker.com / v2 / search / repositories /?query = * & page_size = 100 & page = 1
        url_images = "https://hub.docker.com/v2/search/repositories/?query=*&page_size="+str(page_size)+"&page="+str(page_n)
        return url_images


    def save_into_db(self, list_image):
        for im in list_image:
            print("[" + im.repo_name + "] saved into db")
            im.save()