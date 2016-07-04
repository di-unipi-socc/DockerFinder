import datetime
from . import utils
from mongoengine import *
import pika
import json

class Crawler:

    def __init__(self, port=5672, rabbit_host='172.17.0.2'):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(rabbit_host, port=port))
        self.channel = self.connection.channel()


    def crawl(self, tot_image=100, page_size=10, page_number=1):
        page_number = page_number
        next = ""
        print("Crawling the images from the docker Hub...")
        crawled_image, saved_images = 0, 0
        while next is not None and tot_image > 0:
            url = self.build_search_url(page_number, page_size)
            json_response = utils.req_to_json(url)
            hub_images = json_response['results']   # 'results' is a list of images
            crawled_image += len(hub_images)
            for im in hub_images:
                image = {}
                list_tags = utils.get_all_tags(im['repo_name'])
                print("[" + im['repo_name'] + "] found tags " + str(len(list_tags)))
                if len(list_tags) > 0 and 'latest' in list_tags:   # if contains "latest" tag will be downloaded
                    print("[" + im['repo_name'] + "] crawled from docker Hub")
                    image['name'] = im['repo_name']
                    image['tags'] = list_tags
                    self.send_to_rabbit(json.dumps(image,sort_keys=True, indent=4))
                    print("[" + im['repo_name'] + "] sent to the rabbit channel")
                    saved_images += 1
            next = json_response['next']
            page_number += 1
            print("\n {0} Crawled images ".format(str(crawled_image)))
            print(" {0} Sent into channel \n".format(str(saved_images)))
            tot_image -= -1

    def build_search_url(self, page_n, page_size=10):
        #https: // hub.docker.com / v2 / search / repositories /?query = * & page_size = 100 & page = 1
        url_images = "https://hub.docker.com/v2/search/repositories/?query=*&page_size="+str(page_size)+"&page="+str(page_n)
        return url_images

    def send_to_rabbit(self, msg, rabbit_queue="dofinder"):
        self.channel.queue_declare(queue=rabbit_queue)
        self.channel.basic_publish(exchange='', routing_key=rabbit_queue, body=msg)
        #print("["+msg+ "] sent into channel "+rabbit_queue)

