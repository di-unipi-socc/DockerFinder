import json
import docker
import re
import os

client_docker= docker.DockerClient(base_url="unix://var/run/docker.sock")

def on_message(repo_name, context):

    logger = context['logger']
    docker_hub = context['hub']
    client_images = context['images']

    logger.info("Received name " + repo_name)

    my_image = dict()

    tag = "latest"
    try:
        # download the Docker image
        list_tags = docker_hub.get_all_tags(repo_name)
        tag = ""
        if "latest" in list_tags:
            tag = "latest"
        elif len(list_tags)>0:
            tag = list_tags[0] # take the first tag



        logger.info("Pulling image {0}:{1} ...".format(repo_name, tag))
        image = client_docker.images.pull(name=repo_name, tag=tag)
        tag = image.tags[0]
        logger.info("{} is  pulled locally.".format(tag))

        my_image['name'] = tag

        # create a infinite running container
        container = client_docker.containers.create(tag, entrypoint="sleep 1000000000")
        # start the container
        container.start()


        # list of software distributions found in the image.
        softwares = []
        with open(os.path.join(os.path.dirname(__file__),'softwares.json')) as json_data:
        #with open('pyfinder/deploy/softwares.json') as json_data:
            software= json.load(json_data)
            for sw in software:# [{'opt':'python --version','regex':'[0-9]+[.][0-9]*[.0-9]*'}]:
                command = sw['name']+" " + sw['cmd']
                # create an exec instance
                res = container.exec_run(cmd=command)
                output = res.decode()
                prog = re.compile(sw['regex'])
                match = prog.search(output)
                if match:
                      version = match.group(0)
                      softwares.append({'software': sw['name'], 'ver': version})
                      logger.debug("{0} {1} found.".format(sw['name'], version))
                else:
                      logger.debug("[{0}] NOT found in ".format(sw['name']))

        #logger.info("{0} {1} found.".format(sw['name'], version))
        logger.info('['+''.join('{} {},'.format(s['software'],s['ver']) for s in softwares)+"]")

        my_image['softwares']  = softwares

        client_images.post_image(my_image)

        container.stop(timeout=2) # after 2 second it stops the container with SIGKILL
        container.remove()
        client_docker.images.remove(image=tag, force=True)
        logger.info("Removed image {0}".format(tag))

    except  docker.errors.APIError as e:
        logger.error(str(e))
    except  docker.errors.ImageNotFound as e:
        logger.error(str(e))
