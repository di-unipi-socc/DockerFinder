import requests
import sys
import urllib.parse
import logging


"""
This module interacts with Docker Hub endpoint.
"""


class ClientHub:

    def __init__(self, docker_hub_endpoint="https://hub.docker.com", path_last_url=None):
        self.docker_hub = docker_hub_endpoint
        self.session = requests.session()
        #self.logger = get_logger(__class__.__name__)
        #self.logger = get_logger(__name__, logging.INFO)
        self.logger =  logging.getLogger(__class__.__name__)
        self.logger.info(__class__.__name__+ " logger initialized.")
        self.next_url = None

        if(path_last_url):
            # file where to save the url:  "/data/crawler/lasturl.txt"
            self.path_file_url = path_last_url

            from_page, page_size= 1, 100  # initial page to start the crawling
            if(self.get_last_url(self.path_file_url) is None):  # if the url is not stored in the file
                init_url = self.build_search_url(page=from_page, page_size=page_size)
                self.logger.info("Init URL:"+init_url)
                self.save_last_url(self.path_file_url, init_url)
                self.next_url  = init_url
            else:
                self.next_url = self.get_last_url(self.path_file_url)

    def get_num_tags(self, repo_name):
        """ Count the number of tags associated with a repository name."""
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
        """
        RGEt  all the tags associated with the repository name.
        :param repo_name: the name of the repository.
        :return: a list of (string) tags name.
        """
        url_tags = self.docker_hub+"/v2/repositories/" + repo_name + "/tags/"
        try:
            #self.logger.info(url_tags)
            res = self.session.get(url_tags)
            self.logger.debug("["+repo_name+"] Getting all the tags")
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
                self.logger.debug(str(res.status_code) +": "+ res.text)
                return []

        except requests.exceptions.ConnectionError as e:
            self.logger.exception("ConnectionError: ")
        except:
            self.logger.exception("Unexpected error:")

    def crawl_images(self, max_images, from_page=1, page_size=100, force_from_page=False, filter_images= lambda repo_name: True):

        """
        This is a generator function that crawls and yield the images' name crawled from Docker Hub.
        :param from_page: page number for starting crawling images. If
        :param page_size: the number of images in a single page.
        :param max_images: the  number of images to be crawled from Docker hub.
         If *None* all the images  of Docker Hub will be crawled [default: None]
        :return:
        """
        if force_from_page:
            self.next_url = self.build_search_url(from_page, page_size)
        elif self.next_url:  # if exist a previous stored url
            self.next_url=  self.get_last_url(self.path_file_url)
        else:
            self.next_url = self.build_search_url(from_page, page_size)
        #else:
        #    self.next_url=  self.get_last_url(self.path_file_url)
        #    #self.build_search_url(page=from_page, page_size=page_size)
        self.logger.info("Next URL="+self.next_url)

        #count = self.count_all_images()
        #max_images = count if not max_images else max_images  # download all images if max_images=None
        crawled_images = 0
        #self.logger.debug("Total images into Docker Hub: " + str(max_images))
        try:
            while self.next_url and crawled_images < max_images: # max_images > 0

                self.save_last_url(self.path_file_url, self.next_url) # save last url

                self.logger.debug("URL="+ self.next_url)
                res = requests.get(self.next_url)
                if res.status_code == requests.codes.ok:
                    json_response = res.json()
                    list_json_image = self._apply_filter(json_response['results'], filter_function=filter_images)
                    self.next_url= json_response['next']
                    temp_images = len(list_json_image)
                    if temp_images + crawled_images > max_images:
                        list_json_image = list_json_image[:max_images-crawled_images]
                    crawled_images += len(list_json_image)
                    yield list_json_image
                else:
                    self.logger.error(str(res.status_code) + " Error response: " + res.text)
            else:
                return

        except requests.exceptions.ConnectionError as e:
            self.logger.exception("ConnectionError: ")
            raise
        except:
            self.logger.exception("Unexpected error:")
            raise

    def save_last_url(self, path, url):
        try:
            with open(path, 'w') as f:
                f.write(url)
                self.logger.debug(url + " saved into "+ path)
        except FileNotFoundError as e:
            self.logger.error(str(e))
            raise

    def get_last_url(self,path):
        ##return an array of two position:[0] page; [1] page-size
        try:
            with open(path, 'r') as f:
                url = f.read()
                self.logger.debug("Read last URL from file: "+ url)
                return url
        except FileNotFoundError as e:
            self.logger.warning("File from reading the last URL not found" + str(e))
            return None



    def _apply_filter(self, list_of_json_images, filter_function):
        """Filters the *list_of_json_images* applying the *filter_function*.  \n
        The *filter_function* take as input an image name and return  \n
        ``True`` if the image must be mantained, ``False`` if the image must be discarded."""
        filtered_images = []
        for image in list_of_json_images:
            repo_name = image['repo_name']
            if filter_function(repo_name):
                filtered_images.append(image)
            else:
                self.logger.debug("["+repo_name+"] negative filtered, not taken")
        return filtered_images

    def build_search_url(self, page, page_size=10):
        # https://hub.docker.com/v2/search/repositories/?query=*&page_size=100&page=1
        params = (('query', '*'), ('page', page), ('page_size', page_size))
        url_encode = urllib.parse.urlencode(params)
        url_images = self.docker_hub+"/v2/search/repositories/?"+url_encode
        return url_images

    def get_json_repo(self, repo_name):
        """Get a the informations present on Docker Hub for a given repository name.
        :return: JSON object with the Docker Hub info for the repository name.

        """
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
        """ Get the informations for the repository with *tag*."""
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
            self.logger.exception("ConnectionError: ")

    def count_all_images(self):
        """ Count all the images stored into Docker Hub"""
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
        """ Crawls only the official repositories"""
        url_repositories = self.docker_hub + "/v2/repositories/library?"
        params = (('page', 1), ('page_size', 100))
        url_encode = urllib.parse.urlencode(params)
        count = 0
        try:
            res = self.session.get(url_repositories+url_encode)
            if res.status_code == requests.codes.ok:
                json_response = res.json()
                list_images = [res['name'] for res in json_response['results']]

                count += json_response['count']
                next_page = json_response['next']
                while next_page:
                    self.logger.info(next_page)
                    res = self.session.get(next_page)
                    json_response = res.json()
                    list_images += [res['name'] for res in json_response['results']]
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

    def is_alive_in_hub(self, repo_name, tag = "latest"):
        image_hub = self.docker_hub+"/v2/repositories/" + repo_name + "/tags/"+tag
        #try:
        res = self.session.get(image_hub)
        if res.status_code == 404:# or res.json()['count'] == 0:
            self.logger.debug(repo_name+":"+tag +" is NOT alive in Docker Hub")
            return False
        elif res.status_code == requests.codes.ok:
            self.logger.debug("["+repo_name+":"+tag +"] is alive in Docker Hub")
            return True
        else:
            return False
