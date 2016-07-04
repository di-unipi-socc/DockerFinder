import docker
import re
import yaml
import os
import datetime
from .container import Container
from .utils import *
import pika

class Scanner:

    def __init__(self, versions_cmd="/../../resources/versions.yml", port=5672, rabbit_host='172.17.0.2'):
        # path of the file containing the command of versions
        self.versionCommands = yaml.load(open(os.path.dirname(__file__) + versions_cmd))
        # sets the docker host from your environment variables
        self.client = docker.Client(**docker.utils.kwargs_from_env(assert_hostname=False))

        # RabbitQm connection
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbit_host,port=port,))
        self.channel = self.connection.channel()

    def run(self, rabbit_queue="dofinder"):

        self.channel.queue_declare(queue=rabbit_queue, durable=True)  # make sure that the channel is created (e.g. if crawler start later)

        def callback(ch, method, properties, body):
            json_res = json.loads(body.decode())

            print(" [x] Received "+json_res['name'] )
            # scanning the images
            self.scan(json_res['name'])

            ## aknowledgment of finish the scanning
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

        image = {}
        print('Scanning [{0}]'.format(repo_name))

        image["repo_name"] = repo_name
        self.info_inspect(repo_name, image)
        self.info_docker_hub(repo_name, image)
        self.info_dofinder(repo_name, image)

        image['last_scan'] = str(datetime.datetime.now())

        if rmi:
            remove_image(repo_name, force=True)
        return image

    def info_inspect(self, repo_name, image):
        """
         docker inspect IMAGE
        """
        print('[{}] docker inspect ... '.format(repo_name))
        dict_inspect = self.client.inspect_image(repo_name)
        image['size'] = dict_inspect['Size']
        #image.size = str(dict_inspect['Size'])

    def info_docker_hub(self, repo_name, image):
        #
        """
        {
            "user": "oliverkenyon",
            "name": "spark_worker",
            "namespace": "oliverkenyon",
            "status": 1,
            "description": "",
            "is_private": false,
            "is_automated": false,
            "can_edit": false,
            "star_count": 0,
            "pull_count": 44,
            "last_updated": "2016-04-27T10:29:50.372403Z",
            "has_starred": false,
            "full_description": null,
            "permissions": {
                "read": true,
                "write": false,
                "admin": false
            }
        }
        """
        # TODO info on tag latest is different from info on repo_name only (last_upadate is different)
        #https://hub.docker.com/v2/repositories/<name>/tags/latest
        print('[{}] docker API ... '.format(repo_name))
        url_tag_latest = "https://hub.docker.com/v2/repositories/" + repo_name + "/tags/latest"
        url_namespace = "https://hub.docker.com/v2/repositories/" + repo_name
        json_response = req_to_json(url_namespace)
        #print(json_response)

        image['description'] = json_response['description']
        image['star_count'] = json_response['star_count']
        image['pull_count'] = json_response['pull_count']
        image['last_updated'] = json_response['last_updated']


    def info_dofinder(self, repo_name, image):


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
                    #image.distro = dist
                    image['distro'] = dist
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
                    #b = Bin(bin=bin, ver=version)
                    #image.bins.append(b)
                    bins.append({'bin':bin,'ver':version})
                #else:
                #    pass
                #    print("[{0}] not found {1}".format(repo_name, bin))
            image['bins'] = bins
            print('[{}] finish search'.format(repo_name))

    def _get_sys(self, yml_cmd):
        apps = yml_cmd['system']
        for app in apps:
            yield app["cmd"], app["re"]

    def _get_bins(self, yml_cmd):
        apps = yml_cmd['applications']
        for app in apps:
            yield app["name"], app["ver"], app["re"]

