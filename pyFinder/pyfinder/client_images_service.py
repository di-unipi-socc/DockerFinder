import requests
import json
import sys
from .utils import *

# if r.status_code == requests.codes.ok:

#Any requests that you make within a session will automatically reuse the appropriate connection!


# r = requests.head(url=url)
# r.links["next"]

class ClientImages:

    def __init__(self, url_api="127.0.0.1:3000/api/images/"):
        # self.connection = http.client.HTTPConnection(host_api, port_api)
        self.session = requests.Session()
        self.url_api = url_api

    def post_image(self, dict_image):
        try:
            res = self.session.post(self.url_api, headers={'Content-type': 'application/json'}, json=dict_image)
            if res.status_code == requests.codes.created or res.status_code == requests.codes.ok:
                print("["+dict_image['repo_name']+"] successfully created into "+res.url)

            else:
                print(str(res.status_code)+" Error code "+res.text)
        except requests.exceptions.ConnectionError as e:
            print("ConnectionError: " + str(e))
        except:
            print("Unexpected error:", sys.exc_info()[0])
            raise
        else:
            return res.json()

    def put_image(self, dict_image):
        try:
            id_image = self.get_id_image(dict_image['repo_name'])
            res = self.session.put(self.url_api+id_image, headers={'Content-type': 'application/json'}, json=dict_image)
            if res.status_code == requests.codes.ok:
                print("[" + dict_image['repo_name'] + "] successfully UPDATED into server")
            else:
                print(str(res.status_code) + " Error code " + res.text)
        except requests.exceptions.ConnectionError as e:
            print("ConnectionError: " + str(e))
        except Exception as e:
            print("Exception" + str(e))
        except:
            print("Unexpected error:", sys.exc_info()[0])
            raise
        else:
            return res.json()

    def get_images(self):
        try:
            res = self.session.get(self.url_api)
            if res.status_code == requests.codes.ok:
                return res.json()
            else:
                print(str(res.status_code) + " Error code. " + res.text)
        except requests.exceptions.ConnectionError as e:
            print("ConnectionError: " + str(e))
        except:
            print("Unexpected error:", sys.exc_info()[0])
            raise

    def get_id_image(self, repo_name):
        json_image_list = self.get_image(repo_name)
        if json_image_list:
            if "_id" in json_image_list[0].keys():
                return json_image_list[0]['_id']
            else:
                raise Exception(" _id not found in "+repo_name)

    def get_image(self, repo_name):
        url = self.url_api + "?repo_name=" + repo_name
        try:
            res = self.session.get(url)
            return res.json()
        except requests.exceptions.ConnectionError as e:
            print("ConnectionError: " + str(e))

    def get_scan_updated(self, repo_name):
        payload = {'repo_name': repo_name, 'select': 'last_scan last_updated'}
        try:
            res = requests.get(self.url_api, params=payload)
            return res.json()
        except requests.exceptions.ConnectionError as e:
            print("ConnectionError: " + str(e))

    def is_new(self, repo_name):
        print( " veryfind that is new the repo"+repo_name)
        return False if self.get_image(repo_name) else True

    def must_scanned(self, repo_name, tag="latest"):
        """
        Check if the repo_name has been scanned recently and don't require another scannerization.
         if(local.last_updated > remote.last_scan )
        :param repo_name:
        :return:
        """
        # info from server api
        res_list_json = self.get_scan_updated(repo_name)
        if res_list_json:   # if not empty list, the result is there
            print(res_list_json)
            image_json = res_list_json[0]
            dofinder_last_scan = string_to_date(image_json['last_scan'])
            dofinder_last_update = string_to_date(image_json['last_updated'])

            # latest_updated from docker hub
            url_tag_latest = "https://hub.docker.com/v2/repositories/" + repo_name + "/tags/" + tag
            json_response = self.session.get(url_tag_latest).json()
            hub_last_update_string = json_response['last_updated']
            hub_last_update = string_to_date(hub_last_update_string)

            # if(hub_last_update > dofinder_last__update && hub_last_update > dofinder_last_scan):
            if hub_last_update > dofinder_last_update:
                #print("[" + repo_name + "] NOT need to update into doFinder, docker hub last updated is less or equal")
                #print(hub_last_update.isoformat() + " is greater than " + dofinder_last_update.isoformat())
                return True
            else:
                #print(hub_last_update.isoformat() + " is less or equal than " + dofinder_last_update.isoformat())
                print("["+repo_name+"] NOT need to scann, doFinder is greater or equal to docker hub last updated")
                return False


