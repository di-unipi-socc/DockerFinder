import docker


def pull_image(image_name, tag="latest"):
    # sets the docker host from your environment variables
    client = docker.Client(**docker.utils.kwargs_from_env(assert_hostname=False))
    # try to set image
    if not image_name:
        ims = client.images()
        if len(ims) >= 1:
            image_name = [im['RepoTags'][0] for im in client.images()][0]

    assert image_name, 'No image given or found locally.'

    # get image if not available locally
    im_names = [im['RepoTags'][0] for im in client.images()]
    if (not any([image_name in imname for imname in im_names])) and client.search(image_name):
        print('Image {} not found locally. Pulling from docker hub.'.format(image_name))
        for line in client.pull(image_name, stream=True):
            print(line.decode())