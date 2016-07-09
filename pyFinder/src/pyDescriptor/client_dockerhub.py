import requests
import sys
class ClientHub:

    def __init__(self, docker_hub_endpoint="https://hub.docker.com/"):
        self.docker_hub = docker_hub_endpoint
        self.session = requests.session()

    def get_count_tags(self, repo_name):
        url_tags = self.docker_hub + "/v2/repositories/" + repo_name + "/tags/"
        try:
            res = self.session.get(url_tags)
            if res.status_code == requests.codes.ok:
                json_response = res.json()
                count = json_response['count']
                return count
        except requests.exceptions.ConnectionError as e:
            print("ConnectionError: " + str(e))


    def get_all_tags(self, repo_name):
        url_tags = self.docker_hub+"/v2/repositories/" + repo_name + "/tags/"
        list_tags = []
        try:
            res = self.session.get(url_tags)
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
            else:
                print(str(res.status_code) +" error response: "+ res.text)
            return list_tags
        except requests.exceptions.ConnectionError as e:
            print("ConnectionError: " + str(e))
        except:
            print("Unexpected error:", sys.exc_info()[0])
            raise

    def crawl_images(self, page=1, page_size=10, max_images=None):
        """
        :param page:
        :param page_size:
        :param max_images: (int) the maximun number of images crawled from the docker hub.
         If None all the images will be crawled. Default None.
        :return:
        """
        url_images = self.build_search_url(page=page, page_size=page_size)
        next_page = None
        try:
            res = requests.get(url_images)
            if res.status_code == requests.codes.ok:
                json_response = res.json()
                next_page = json_response['next']
                count = json_response['count']
                max_images = count if not max_images else max_images  # download all images if max_images=None
            else:
                print(str(res.status_code) + " error response: " + res.text)
            print("[Crawler] total images to crawl: "+str(max_images))
            while next_page and max_images:         # there is another page and max_images >0
                res = requests.get(url_images)
                if res.status_code == requests.codes.ok:
                    json_response = res.json()
                    list_json_image = json_response['results']
                    next_page = json_response['next']
                    page +=1
                    max_images -= len(list_json_image)
                    url_images = self.build_search_url(page=page, page_size=page_size)
                else:
                    print(str(res.status_code) + " error response: " + res.text)
                    return
                yield list_json_image
        except requests.exceptions.ConnectionError as e:
            print("ConnectionError: " + str(e))
        except:
            print("Unexpected error:", sys.exc_info()[0])
            raise

    def build_search_url(self, page, page_size=10):
        # https://hub.docker.com/v2/search/repositories/?query=*&page_size=100&page=1
        url_images = "https://hub.docker.com/v2/search/repositories/?query=*&page_size=" + str(
            page_size) + "&page=" + str(page)
        return url_images
