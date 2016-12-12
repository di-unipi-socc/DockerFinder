import requests
import json
import sys
from .dfexception import *
import logging
from urllib.parse import urljoin
from .utils import  string_to_date
""" This module interacts with the *Images service* running on the *storage* part."""

class ClientImages:

    def __init__(self, images_url):
        self.session = requests.Session()
        self.url_api = images_url

        self.logger = logging.getLogger(__class__.__name__)
        self.logger.info(__class__.__name__ + " logger  initialized")
        self.logger.info("Images server: "+self.url_api)

    def post_image(self, dict_image):
        """Add an image description"""
        try:
            self.logger.debug("POST "+ str(dict_image)+"  into  "+self.url_api)
            res = self.session.post(self.url_api, headers={'Content-type': 'application/json'}, json=dict_image)
            if res.status_code == requests.codes.created or res.status_code == requests.codes.ok:
                self.logger.debug("POST ["+dict_image['name']+"]  into  "+res.url)
            else:
                self.logger.error(str(res.status_code)+": "+res.text)
        except requests.exceptions.ConnectionError as e:
            self.logger.exception("ConnectionError: ")
        except:
            self.logger.exception("Unexpected error:")


    def put_image(self, dict_image):
        """Update an image description"""
        try:
            id_image = self.get_id_image(dict_image['name'])
            res = self.session.put(self.url_api+id_image, headers={'Content-type': 'application/json'}, json=dict_image)
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
            #id_image = self.get_id_image(dict_image['name'])
            dict_status = { "status": status }
            url = ''
            if  self.url_api[len(self.url_api)-1] == "/":
                url = self.url_api+id_image
            else:
                url = self.url_api+"/"+id_image
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
            res = self.session.get(self.url_api, params=payload)
            res_json = res.json()
            images = res_json['images']
            if res_json['count'] == 1:
                return images[0]  # return the first image object
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
            res_json = self.get_image(repo_name)
            ## Return the json or raise an exception if does not exist
            self.logger.debug("[" + repo_name + "] found within local database")
            return False
        except ImageNotFound as e:
            self.logger.debug(str(e))
            return True

    def delete_image(self, image_id):
        try:
            url_image_id =self.url_api + "/"+image_id
            res = self.session.delete(url_image_id)
            if res.status_code == 204:
                self.logger.debug("DELETE [" + image_id + "] found within local database")
                #print("Deleted ", image_id)
                #return res.json()
            else:
                self.logger.error(str(res.status_code) + " Error code. " + res.text)
                #print(str(res.status_code) + " Error code. " + res.text)
        except requests.exceptions.ConnectionError as e:
             self.logger.exception("ConnectionError: ")
             #print("ConnectionError: ")
        except:
            self.logger.exception("Unexpected error:")
            raise


    def must_scanned(self, name):#, tag="latest"):
        """
        Check if the *repo_name* has been scanned recently and it is not require the scan.
         if(local.last_updated > remote.last_scan ) then {scan}
        :param repo_name: the image name with tag.
        :return: True if the image must be scan. False otherwise.
        """
        tag = name.split(":")[1]
        repo = name.split(":")[0]
        res_image_json = self.get_scan_updated(name)  # {"images:[
        if res_image_json is not None:   # if not empty list, the result is there
            #self.logger.debug("Received from Images service" + str(res_image_json))
            image_json = res_image_json['images'][0]
            self.logger.debug("[" + name + "] local: last scan: " + str(image_json['last_scan']) + "; last update: " + str(image_json[
                'last_updated']))
            dofinder_last_scan = string_to_date(image_json['last_scan'])
            if image_json['last_updated']:
                dofinder_last_update = string_to_date(image_json['last_updated'])
            else:
                dofinder_last_update = dofinder_last_scan   # if is None tha image is not scan again becuse is  equal to last scan

            # latest_updated from docker hub
            url_tag_latest = "https://hub.docker.com/v2/repositories/" + repo + "/tags/" + tag
            json_response = self.session.get(url_tag_latest).json()
            hub_last_update_string = json_response['last_updated']
            if(json_response['last_updated']):
                hub_last_update = string_to_date(hub_last_update_string)
            else:
                hub_last_update = dofinder_last_scan

            # if(hub_last_update > dofinder_last__update && hub_last_update > dofinder_last_scan):
            if hub_last_update > dofinder_last_update or  hub_last_update > dofinder_last_scan:
                self.logger.debug("[" + name + "] need to update, last update of docker Hub is greater than last scan")
                return True
            else:
                self.logger.debug("["+name+"] NOT need to update: Hub last update:"+str(hub_last_update)+" local last upate:" +str(dofinder_last_update))
