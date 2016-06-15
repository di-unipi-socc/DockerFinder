import urllib.request
import json
import datetime
from mongoengine import *
from .model.hub import Hub
from .model.image import Image


class Crawler:

    def __init__(self, alias_db, host='localhost', port=27017):
        self.url = "https://hub.docker.com/v2/search/repositories/?query=*&page="
        self.host = host
        self.alias_db = alias_db
        connect(alias_db, host=host, port=port)

    def crawl(self):
        i = 1
        next = ""
        print("Crawling the images from the docker hub")
        while next is not None and i != 5 :
            response = urllib.request.urlopen(self.url+str(i)).read()
            json_response = json.loads(response.decode())
            # 'results' is a list of 10 images
            self.extract_info(json_response['results'])
            next = json_response['next']
            i+=1

    def extract_info(self, images_list):
        list_image = []
        hub = Hub()
        for im in images_list:
            image = Image(repo_name_tag=im['repo_name'])
            print("crawling "+im['repo_name'])
            if im['pull_count']:
                hub.pull = im['pull_count']
            if im['star_count']:
                hub.stars = im['star_count']
            if im['is_official']:
                hub.is_official = im['is_official']
            if im['is_automated']:
                hub.is_automated = im['is_automated']
            if im['short_description']:
                hub.short_description = im['short_description']
            if im['repo_owner']:
                hub.repo_owner = im['repo_owner']
            image.hub = hub
            image.t_crawl = datetime.datetime.now
            list_image.append(image)
        for im in list_image:
            im.save()
            print("Inserted "+im.repo_name_tag)

