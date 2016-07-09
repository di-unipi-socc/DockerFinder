import docker
import re
import yaml
import os
import datetime
import time
from .container import Container
from .utils import *
from .client_api import  ClientApi
import pika

class Scanner:

    def __init__(self, versions_cmd="/../../resources/versions.yml", port_rabbit=5672, host_rabbit='172.17.0.2', url_api="127.0.0.1:8000/api/images"):
        # path of the file containing the command of versions
        self.versionCommands = yaml.load(open(os.path.dirname(__file__) + versions_cmd))
        # sets the docker host from your environment variables
        self.client = docker.Client(**docker.utils.kwargs_from_env(assert_hostname=False))

        # RabbitQm connection
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=host_rabbit, port=port_rabbit))
        self.channel = self.connection.channel()

        # the clientApi talks with the server api in order to post the image description
        self.client_api = ClientApi(url_api=url_api)

    def run(self, rabbit_queue="dofinder"):

        # TODO: rabbitQm server can be down. check and retry on orde to connect
        self.channel.queue_declare(queue=rabbit_queue, durable=True)  # make sure that the channel is created (e.g. if crawler start later)

        def callback(ch, method, properties, body):
            json_res = json.loads(body.decode())
            repo_name = json_res['name']
            print("[scanner] Received " + repo_name)
            # scann the image received from the queue

            #res_list_image = self.client_api.get_image(repo_name)
            if self.client_api.is_new(repo_name):           # the image is totally new
                dict_image = self.scan(repo_name)
                self.client_api.post_image(dict_image)      # POST the description of the image
            elif self.client_api.must_scanned(repo_name):   # the image must be scan again
                dict_image = self.scan(repo_name)
                self.client_api.put_image(dict_image)       # PUT the new image description of the image
            else:
                print("["+repo_name+"] not scannerized")

            ## aknowledgment of finish the scanning to the rabbitMQ server
            ch.basic_ack(delivery_tag=method.delivery_tag)
            #print(" [x] Finish scann%r" % body )

        self.channel.basic_qos(prefetch_count=1)
        self.channel.basic_consume(callback, queue=rabbit_queue, no_ack=True)
        print(' [scanner] Waiting for messages. To exit press CTRL+C')

        self.channel.start_consuming()

    def scan(self, repo_name, tag="latest", rmi=False):
        """

        :param repo_name:
        :param tag:
        :param rmi:
        :return: a dictionary with the description of the image identified by repo_name.
        """
        pull_image(repo_name, tag)

        dict_image = {}
        print('Scanning [{0}]'.format(repo_name))

        dict_image["repo_name"] = repo_name

        self.info_inspect(repo_name, dict_image)
        self.info_docker_hub(repo_name, dict_image)
        self.info_dofinder(repo_name, dict_image)

        print('[{0}] finish scanning'.format(repo_name))
        dict_image['last_scan'] = str(datetime.datetime.now())
        if rmi:
            remove_image(repo_name, force=True)
        return dict_image

    def info_inspect(self, repo_name, dict_image):
        """
         docker inspect IMAGE
        """
        print('[{}] docker inspect ... '.format(repo_name))
        dict_inspect = self.client.inspect_image(repo_name)
        #dict_image['size'] = dict_inspect['Size']


    def info_docker_hub(self, repo_name, dict_image):
        """
        Download the image information among Docker API v2.
        :param repo_name:
        :param dict_image:
        :return:
        """
        print('[{}] docker API ... '.format(repo_name))

        url_namespace = "https://hub.docker.com/v2/repositories/" + repo_name
        json_response = req_to_json(url_namespace)
        print(json_response)
        dict_image['description'] = json_response['description']
        dict_image['star_count'] = json_response['star_count']
        dict_image['pull_count'] = json_response['pull_count']

        url_tag_latest = "https://hub.docker.com/v2/repositories/" + repo_name + "/tags/latest"
        json_response = req_to_json(url_tag_latest)
        dict_image['last_updated'] = json_response['last_updated']
        dict_image['full_size'] =json_response['full_size']

    def info_dofinder(self, repo_name, dict_image):

        print('[{}] searching binaries version ... '.format(repo_name))

        try:
            with Container(repo_name) as c:
                # search distribution
                for cmd, reg in self._get_sys(self.versionCommands):
                    output = c.run(cmd)
                    p = re.compile(reg)
                    match = p.search(output)
                    if match:
                        # take the non-capturing group: only the matches, group[0] return all the match
                        dist = match.group(0)
                        dict_image['distro'] = dist
                    else:
                        print("[{0}] not found {1}".format(repo_name, cmd))

            with Container(repo_name) as c:
                # search binary versions
                bins = []
                for bin, cmd, regex in self._get_bins(self.versionCommands):
                    #print("[{}] searching {} ".format(image, bin))
                    output = c.run(bin+" "+cmd)
                    p = re.compile(regex)     # can be saved the compilatiion of the regex to savee time (if is equal to all the version)
                    match = p.search(output)
                    if match:
                        version = match.group(0)
                        print("[{0}] found {1}: {2}".format(repo_name, bin, version))
                        bins.append({'bin':bin,'ver':version})
                    #else:
                    #    pass
                    #    print("[{0}] not found {1}".format(repo_name, bin))
                dict_image['bins'] = bins
        except docker.errors.APIError as e:
            print("Error"+str(e))
    def _get_sys(self, yml_cmd):
        apps = yml_cmd['system']
        for app in apps:
            yield app["cmd"], app["re"]

    def _get_bins(self, yml_cmd):
        apps = yml_cmd['applications']
        for app in apps:
            yield app["name"], app["ver"], app["re"]

