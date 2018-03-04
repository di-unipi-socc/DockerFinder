import requests
import json
import sys
from .dfexception import *
import logging
from urllib.parse import urljoin
from  requests.compat import urljoin
from .utils import  string_to_date
""" This module interacts with the *Images service* running on the *storage* part."""

class ClientImages:

    def __init__(self, images_url):
        self.session = requests.Session()
        # self.url_api = images_url
        self.url_api  = images_url+"/" if images_url[len(images_url)-1] != "/" else images_url # add blacklash at the end of the url

        self.logger = logging.getLogger(__class__.__name__)
        self.logger.info(__class__.__name__ + " logger  initialized")
        self.logger.info("Images server: "+self.url_api)

    def post_image(self, dict_image):
        """Add an image description"""
        try:
            self.logger.info("POST {} url: {}".format(dict_image['name'],self.url_api))
             # requests.post(url, data=json.dumps(payload))
            self.logger.info(json.dumps(dict_image))
            res = self.session.post(self.url_api, data=json.dumps(dict_image), headers={'Content-type': 'application/json'})#, json=dict_image)
            if res.status_code == requests.codes.created or res.status_code == requests.codes.ok:
                self.logger.debug("POST ["+dict_image['name']+"]  into  "+res.url)
            else:
                self.logger.error(str(res.status_code)+" body: "+ str(res.json()))
                raise Exception("POST  error")
        except requests.exceptions.ConnectionError as e:
            self.logger.exception("ConnectionError: ")
        except:
            self.logger.exception("Unexpected error:")


    def put_image(self, dict_image):
        """Update an image description"""
        try:
            id_image = self.get_id_image(dict_image['name'])
            url = urljoin(self.url_api,str(id_image))
            self.logger.info("PUT {} ".format(url) )
            res = self.session.put(url, headers={'Content-type': 'application/json'}, json=dict_image)
            if res.status_code == requests.codes.ok:
                self.logger.debug("PUT [" + dict_image['name'] + "] into "+res.url)
            else:
                self.logger.error(str(res.status_code) + ": " + res.text)
        except ImageNotFound as e:
            self.logger.exception(str(e))
            raise  e
        except requests.exceptions.ConnectionError as e:
            self.logger.exception("ConnectionError: " )
            raise e
        except:
            self.logger.exception("Unexpected error:")
            raise

    def update_status(self, id_image, status):
        try:
            dict_status = { "status": status }
            url = urljoin(self.url_api,str(id_image))
            self.logger.info("PUT update status {}".format(url))
            res = self.session.put(url, headers={'Content-type': 'application/json'}, json=dict_status)
            if res.status_code == requests.codes.ok:
                self.logger.debug("UPDATED  ["+ res.json()['name'] +" status: "+status)
            else:
                self.logger.error(str(res.status_code) + ": " + res.text)
        except requests.exceptions.ConnectionError as e:
            self.logger.exception("ConnectionError: " )
            raise e
        except:
            self.logger.exception("Unexpected error:")
            raise

    def get_images(self):
        """Get all the images descriptions."""
        try:
            res = self.session.get(self.url_api)
            if res.status_code == requests.codes.ok:
                return res.json()
            else:
                self.logger.error(str(res.status_code) + " Error code. " + res.text)
        except requests.exceptions.ConnectionError as e:
            self.logger.exception("ConnectionError: ")
        except:
            self.logger.exception("Unexpected error:")
            raise

    def get_id_image(self, repo_name):
        """
        Return the *id* of the *repo_name*.
        """
        try:
            json_image = self.get_image(repo_name)
            if "_id" in json_image:
                return json_image['_id']
            else:
                raise ImageNotFound(" _id not found in "+repo_name)
        except ImageNotFound as e:
            raise

    def get_image(self, repo_name):
        """Return the description of a single image"""
        #url = self.url_api + "?name=" + repo_name
        # {"count": 1,  "images": []}
        try:
            payload = {'name': repo_name}
            res_json = self.session.get(self.url_api, params=payload).json()
            # self.logger.info("{}".format(res_json))
            if res_json['count'] > 0:
                return res_json['images'][0] #['images'][0]  # return the first image object
            else:
                raise ImageNotFound("Image "+ repo_name + " not found")
        except requests.exceptions.ConnectionError as e:
            self.logger.exception("ConnectionError: ")

    def get_scan_updated(self, repo_name):
        payload = {'name': repo_name, 'select': 'last_scan last_updated'}
        try:
            res = requests.get(self.url_api, params=payload)
            return res.json()
        except requests.exceptions.ConnectionError as e:
            self.logger.exception("ConnectionError: " )

    def is_new(self, repo_name):
        """Check if the image is new into the images service. \n
        An image is new if it is not present."""
        try:
            self.logger.debug("[" + repo_name + "] is new ?")
            res_json = self.get_image(repo_name)
            self.logger.debug("[" + repo_name + "] found within local database")
            return False
        except ImageNotFound as e:
            self.logger.debug(str(e))
            return True

    def delete_image(self, image_id):
        try:
            url = urljoin(self.url_api,str(id_image))
            self.logger.info("DELETE {}".format(url))
            res = self.session.delete(url)
            if res.status_code == 204:
                self.logger.debug("DELETE [" + image_id + "] into local database")
            else:
                self.logger.error(str(res.status_code) + " Error code. " + res.text)
        except requests.exceptions.ConnectionError as e:
             self.logger.exception("ConnectionError: ")
             raise e
        except:
            self.logger.exception("Unexpected error:")
            raise

    # TODO crate method for checkein if a image must be scanned gain
    def must_scanned(self, name, remote_last_update):#, tag="latest"):
        """
        :param repo_name: the image name with tag.
        :return: True if the image must be scan. False otherwise.
        """
        tag = name.split(":")[1]
        repo = name.split(":")[0]
        must_scanned = True

        res_image_json = self.get_scan_updated(name) # local "last_scan" and "last_update"
        if res_image_json is not None:   # if not empty list, the result is there
            image_json = res_image_json['images'][0]
            try:
                self.logger.info("[" + name + "] local: last scan: " + str(image_json['last_scan']) + "; last update: " + str(image_json[
                    'last_updated']))

                dofinder_last_scan = string_to_date(image_json['last_scan'])
                if image_json['last_updated']:
                    dofinder_last_update = string_to_date(image_json['last_updated'])
                else:
                    dofinder_last_update = dofinder_last_scan   # if is None tha image is not scan again becuse is  equal to last scan

                if string_to_date(remote_last_update) <= dofinder_last_scan or string_to_date(remote_last_update) <= dofinder_last_update:
                    must_scanned = False
            except TypeError:
                raise
            return must_scanned

            # latest_updated from docker hub
            # url_tag_latest = "https://hub.docker.com/v2/repositories/" + repo + "/tags/" + tag
            # json_response = self.session.get(url_tag_latest).json()
            # hub_last_update_string = json_response['last_updated']
            # if(json_response['last_updated']):
            #     hub_last_update = string_to_date(hub_last_update_string)
            # else:
            #     hub_last_update = dofinder_last_scan
            #
            # # if(hub_last_update > dofinder_last__update && hub_last_update > dofinder_last_scan):
            # if hub_last_update > dofinder_last_update or hub_last_update > dofinder_last_scan:
            #     self.logger.debug("[" + name + "] need to update, last update of docker Hub is greater than last scan")
            #     return True
            # else:
            #     self.logger.debug("["+name+"] NOT need to update: Hub last update:"+str(hub_last_update)+" local last upate:" +str(dofinder_last_update))
