import docker
import re
import yaml
import os
import datetime
import time
from .container import Container
from .utils import *
from .client_api import  ClientApi
from .client_dockerhub import ClientHub
import pika

class Scanner:

    def __init__(self, versions_cmd="/resources/versions.yml", port_rabbit=5672, host_rabbit='172.17.0.2', url_imagesservice="http://127.0.0.1:8000/api/images"):

        # path of the file containing the command of versions
        self.versionCommands = yaml.load(open(os.path.dirname(__file__) + versions_cmd))

        # sets the docker host from your environment variables
        # environment-file: key=value

        #f = docker.utils.kwargs_from_env(assert_hostname=False)
        #-v / var / run / docker.sock: / var / run / dockerhost / docker.sock
        self.client = docker.Client(**docker.utils.kwargs_from_env(assert_hostname=False))
        #self.client = docker.Client(base_url='unix://var/run/docker.sock')#**docker.utils.kwargs_from_env(assert_hostname=False))

        # RabbitQm connection
        self.host_rabbit = host_rabbit
        self.port_rabbit = port_rabbit
        # self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=host_rabbit, port=port_rabbit))
        # self.channel = self.connection.channel()

        # the clientApi talks with the server api in order to post the image description
        self.client_api = ClientApi(url_api=url_imagesservice)

        # the clienthub interacts with the dockerHub registry
        self.clientHub = ClientHub()

    def run(self, rabbit_queue="dofinder"):
        print("[scanner] connecting to " + self.host_rabbit + ":" + str(self.port_rabbit) + "...")
        try:
            self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.host_rabbit, port=self.port_rabbit))
            self.channel = self.connection.channel()
        except pika.exceptions.ConnectionClosed as e:
            print("[scanner] error:" + str(e))
            return

        # TODO: rabbitQm server can be down. check and retry on orde to connect
        self.channel.queue_declare(queue=rabbit_queue, durable=True)  # make sure that the channel is created (e.g. if crawler start later)

        def on_message(ch, method, properties, body):
            repo_name = body.decode()
            print("[scanner] Received " + repo_name)
            if self.client_api.is_new(repo_name):           # the image is totally new

                dict_image = self.scan(repo_name)
                self.client_api.post_image(dict_image)      # POST the description of the image
                print("[" + repo_name + "] scan uploaded")
            elif self.client_api.must_scanned(repo_name):   # the image must be scan again
                dict_image = self.scan(repo_name)
                self.client_api.put_image(dict_image)       # PUT the new image description of the image
                print("[" + repo_name + "] scan refresh uploaded")
            else:
                print("["+repo_name+"] scan already up to date.")

            # aknowledgment of finish the scanning to the rabbitMQ server
            ch.basic_ack(delivery_tag=method.delivery_tag)

        self.channel.basic_qos(prefetch_count=1)
        self.channel.basic_consume(on_message, queue=rabbit_queue, no_ack=True)
        print(' [scanner] Waiting for messages. To exit press CTRL+C')
        try:
            self.channel.start_consuming()
        except KeyboardInterrupt:
            self.channel.stop_consuming()
        self.channel.close()

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
        print('[{}] adding Docker Hub info ... '.format(repo_name))

        json_response = self.clientHub.get_json_repo(repo_name)

        dict_image['description'] = json_response['description']
        dict_image['star_count'] = json_response['star_count']
        dict_image['pull_count'] = json_response['pull_count']


        # TODO : here must be included the tags lists of the image
        #josn_reposnse = slef.clientHub.get_all_tags(repo_name)

        json_response = self.clientHub.get_json_tag(repo_name, tag="latest")

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

