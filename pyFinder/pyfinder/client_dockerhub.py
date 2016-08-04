import requests
import sys
import urllib.parse
import logging
from .utils import get_logger


class ClientHub:

    def __init__(self, docker_hub_endpoint="https://hub.docker.com/"):
        self.docker_hub = docker_hub_endpoint
        self.session = requests.session()
        self.logger = get_logger(__name__, logging.INFO)

    def get_num_tags(self, repo_name):
        url_tags = self.docker_hub + "/v2/repositories/" + repo_name + "/tags/"
        try:
            res = self.session.get(url_tags)
            if res.status_code == requests.codes.ok:
                json_response = res.json()
                count = json_response['count']
                return count
        except requests.exceptions.ConnectionError as e:
            self.logger.exception("ConnectionError: ")

    def get_all_tags(self, repo_name):
        url_tags = self.docker_hub+"/v2/repositories/" + repo_name + "/tags/"
        try:
            res = self.session.get(url_tags)
            self.logger.info("["+repo_name+"] Getting all the tags")
            if res.status_code == requests.codes.ok:
                json_response = res.json()
                count = json_response['count']
                list_tags = [res['name'] for res in json_response['results']]  # get the tags in the current page
                next_page = json_response['next']
                while next_page:                                                # pagination of the tags
                    res = self.session.get(next_page)
                    json_response = res.json()
                    list_tags += [res['name'] for res in json_response['results']]
                    next_page = json_response['next']
                return list_tags
            else:
                self.logger.error(str(res.status_code) +" error response: "+ res.text)
                return []

        except requests.exceptions.ConnectionError as e:
            self.logger.exception("ConnectionError: ")
        except:
            self.logger.exception("Unexpected error:")

    def crawl_images(self, page=1, page_size=10, max_images=None, only_tag_latest=True):
        """
        :param page:
        :param page_size:
        :param max_images: (int) the maximun number of images crawled from the docker hub.
         If None all the images will be crawled [default: None]
        :return:
        """
        url_next_page = self.build_search_url(page=page, page_size=page_size)
        count = self.count_all_images()
        max_images = count if not max_images else max_images  # download all images if max_images=None
        crawled_images = 0
        self.logger.info("Total images to crawl: " + str(max_images))
        try:
            while url_next_page and max_images > 0:
                self.logger.debug("GET to "+url_next_page)
                res = requests.get(url_next_page)
                if res.status_code == requests.codes.ok:
                    json_response = res.json()
                    list_json_image = json_response['results']
                    url_next_page = json_response['next']
                    page += 1
                    max_images -= len(list_json_image)
                    yield list_json_image
                else:
                    self.logger.error("Crawl_images method:" +str(res.status_code) + " Error response: " + res.text)
                    #return []

        except requests.exceptions.ConnectionError as e:
            self.logger.exception("ConnectionError: ")
        except:
            self.logger.exception("Unexpected error:")

    def build_search_url(self, page, page_size=10):
        # https://hub.docker.com/v2/search/repositories/?query=*&page_size=100&page=1
        params = (('query', '*'), ('page', page), ('page_size', page_size))
        url_encode = urllib.parse.urlencode(params)
        url_images = self.docker_hub+"/v2/search/repositories/?"+url_encode
        return url_images

    def get_json_repo(self, repo_name):
        url_namespace = self.docker_hub+"/v2/repositories/" + repo_name
        try:
            res = self.session.get(url_namespace)
            if res.status_code == requests.codes.ok:
                json_response = res.json()
                return json_response
            else:
                self.logger.error("Error response: "+str(res.status_code) +": " + res.text)
                return {}
        except requests.exceptions.ConnectionError as e:
            self.logger.exception("ConnectionError: ")

    def get_json_tag(self, repo_name, tag="latest"):
        url_tag = self.docker_hub+"/v2/repositories/" + repo_name + "/tags/"+tag
        try:
            res = self.session.get(url_tag)
            if res.status_code == requests.codes.ok:
                json_response = res.json()
                return json_response
            else:
                self.logger.error(str(res.status_code) + " error response: " + res.text)
                return {}
        except requests.exceptions.ConnectionError as e:
            self.logger.exception("ConnectionError: " )

    def count_all_images(self):
        url_hub = self.build_search_url(page_size=10, page=1)
        try:
            res = self.session.get(url_hub)
            if res.status_code == requests.codes.ok:
                json_response = res.json()
                return json_response['count']
            else:
                self.logger.error(str(res.status_code) + " error response: " + res.text)
                return
        except requests.exceptions.ConnectionError as e:
            self.logger.exception("ConnectionError: " )

    def crawl_official_images(self):
        #https://hub.docker.com/v2/repositories/library
        url_repositories = self.docker_hub + "/v2/repositories/library?"
        params = (('page', 1), ('page_size', 100))
        url_encode = urllib.parse.urlencode(params)
        count = 0
        try:
            res = self.session.get(url_repositories+url_encode)
            if res.status_code == requests.codes.ok:
                json_response = res.json()
                list_images =[res['user']+"/"+res['name'] for res in json_response['results']]
                count += json_response['count']
                next_page = json_response['next']
                while next_page:
                    res = self.session.get(next_page)
                    json_response = res.json()
                    list_images += [res['user']+"/"+res['name'] for res in json_response['results']]
                    next_page = json_response['next']
                return list_images
            else:
                self.logger.error(str(res.status_code) + " error response: " + res.text)
                return []
        except requests.exceptions.ConnectionError as e:
            self.logger.exception("ConnectionError: " + str(e))


    def get_dockerhub(self, path_url):
        url_repositories = self.docker_hub + path_url
        res =self.session.get(url_repositories)
        try:
            if res.status_code == requests.codes.ok:
                json_response = res.json()
                return json_response
            else:
                self.logger.error(str(res.status_code) + "error response: " + res.text)
                return []
        except requests.exceptions.ConnectionError as e:
            self.logger.exception("ConnectionError: " + str(e))

