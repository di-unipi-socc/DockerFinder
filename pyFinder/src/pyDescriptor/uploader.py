import http.client
import urllib.parse
import json


class Uploader:

    def __init__(self, api_server="127.0.0.1", port=None):
        self.connection = http.client.HTTPConnection(api_server, port)
        self.base_url = "/api/images"

    def post_image(self, dict_image):
        json_image = json.dumps(dict_image, indent=4)
        print(json_image)
        headers = {'Content-type': 'application/json'}
        self.connection.request('POST', self.url, json_image, headers)
        response = self.connection.getresponse();
        print("["+dict_image['repo_name']+"] posted to "+self.connection.host)
        return json.loads(response.read().decode())


    def get(self, url):
        try:
            self.connection.request('GET', url)
            http_response = self.connection.getresponse()
            print(http_response.status, http_response.reason)
            return http_response
        except urllib.error.HTTPError as e:
            print(e.code + e.reason)


    def get_images(self):
        return self.get(self.base_url)

    def get_image(self, repo_name):
        url = self.base_url + "?repo_name=" + repo_name
        return self.get(url)

    def get_scan_updated(self, repo_name):
        params = urllib.parse.urlencode({'repo_name': repo_name, 'select': 'last_scan last_updated'})
        response = self.get(self.base_url+"?"+params)
        return response




