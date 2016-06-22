import http.client
import json


class Client:

    def __init__(self, host, port=None):
        self.connection = http.client.HTTPConnection(host, port)

    def post_image(self, dict_image, url="/api/images"):
        json_image = json.dumps(dict_image, indent=4)
        headers = {'Content-type': 'application/json'}
        self.connection.request('POST', url, json_image, headers)
        response = self.connection.getresponse();
        print(dict_image)
        print("["+dict_image['repo_name']+"] posting to "+self.connection.host)
        return response.read().decode()

