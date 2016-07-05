import docker
import re
import yaml
import os
import datetime
import time
from .container import Container
from .utils import *
from . import uploader
import pika

class Scanner:

    def __init__(self, versions_cmd="/../../resources/versions.yml", port=5672, rabbit_host='172.17.0.2'):
        # path of the file containing the command of versions
        self.versionCommands = yaml.load(open(os.path.dirname(__file__) + versions_cmd))
        # sets the docker host from your environment variables
        self.client = docker.Client(**docker.utils.kwargs_from_env(assert_hostname=False))

        # RabbitQm connection
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbit_host, port=port,))
        self.channel = self.connection.channel()

        # the upload talk with the server api
        self.uploader = uploader.Uploader('127.0.0.1', 3000)

    def run(self, rabbit_queue="dofinder"):

        self.channel.queue_declare(queue=rabbit_queue, durable=True)  # make sure that the channel is created (e.g. if crawler start later)

        def callback(ch, method, properties, body):
            json_res = json.loads(body.decode())

            print(" [x] Received "+json_res['name'] )
            repo_name =json_res['name']
            # scanning the images
            if(not self.is_new(repo_name)):
                self.scan(json_res['name'])
            elif (self.must_scanned(repo_name=repo_name)): #not new and not to be scanned
                self.scan(json_res['name'])
            else:
                print("not scanned"+repo_name)

            ## aknowledgment of finish the scanning to the rabbitMQ server
            ch.basic_ack(delivery_tag=method.delivery_tag)
            #print(" [x] Finish scann%r" % body )

        self.channel.basic_qos(prefetch_count=1)
        self.channel.basic_consume(callback, queue=rabbit_queue, no_ack=True)
        print(' [*] Waiting for messages. To exit press CTRL+C')

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
        dict_image['description'] = json_response['description']
        dict_image['star_count'] = json_response['star_count']
        dict_image['pull_count'] = json_response['pull_count']

        url_tag_latest = "https://hub.docker.com/v2/repositories/" + repo_name + "/tags/latest"
        json_response = req_to_json(url_tag_latest)
        dict_image['last_updated'] = json_response['last_updated']
        dict_image['full_size'] =json_response['full_size']

    def info_dofinder(self, repo_name, dict_image):

        local_repo = [im['RepoTags'][0].split(':')[0] for im in self.client.images()]
        if repo_name not in local_repo:
            print('No image found locally.')
            return

        print('[{}] searching binaries version ... '.format(repo_name))

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

            # search binary versions
            bins = []
            for bin, cmd, regex in self._get_bins(self.versionCommands):
                #print("[{}] searching {} ".format(image, bin))
                output = c.run(bin+" "+cmd)
                p = re.compile(regex)     # can be saved the compilatiion of the regex to savee time (if is equal to all the version)
                match = p.search(output)
                if match:
                    version = match.group(0)
                    print("[{0}] found {1}".format(repo_name, bin))
                    bins.append({'bin':bin,'ver':version})
                #else:
                #    pass
                #    print("[{0}] not found {1}".format(repo_name, bin))
            dict_image['bins'] = bins
            print('[{}] finish search'.format(repo_name))

    def _get_sys(self, yml_cmd):
        apps = yml_cmd['system']
        for app in apps:
            yield app["cmd"], app["re"]

    def _get_bins(self, yml_cmd):
        apps = yml_cmd['applications']
        for app in apps:
            yield app["name"], app["ver"], app["re"]

    def is_new(self, repo_name, tag="latest"):
        """
        Check if the repo name exist in the servera pi, if it is already uploaded
        :param repo_name:
        :param tag:
        :return:
        """
        response = self.uploader.get_image(repo_name)
        json_image_list = json.loads(response.read().decode())
        return True if json_image_list else False

    def must_scanned(self, repo_name, tag="latest"):
        """
        Check if the repo_name has been scanned recently and don't require another scannerization.
         if(local.last_updated > remote.last_scan )
        :param repo_name:
        :return:
        """


        # info from server api
        response = self.uploader.get_scan_updated(repo_name)

        json_image_list = json.loads(response.read().decode())

        for im in json_image_list:

            dofinder_last_scan = string_to_date(im['last_scan'])
            dofinder_last_update = string_to_date(im['last_updated'])

            # info from docker hub
            url_tag_latest = "https://hub.docker.com/v2/repositories/" + repo_name + "/tags/"+tag
            json_response = req_to_json(url_tag_latest)
            hub_last_update_string = json_response['last_updated']
            hub_last_update = string_to_date(hub_last_update_string)

            #if(hub_last_update > dofinder_last__update && hub_last_update > dofinder_last_scan):
            if (hub_last_update > dofinder_last_update):
                print(hub_last_update.isoformat() +" id greater than "+dofinder_last_update.isoformat())
                return True
            else:
                print(hub_last_update.isoformat() + " is less than " + dofinder_last_update.isoformat())
                return False


