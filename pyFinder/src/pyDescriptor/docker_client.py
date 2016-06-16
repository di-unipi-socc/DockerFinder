import docker


def pull_image(repo_name, tag="latest"):
    # sets the docker host from your environment variables
    client = docker.Client(**docker.utils.kwargs_from_env(assert_hostname=False))
    # try to set image
    if not repo_name:
        ims = client.images()
        if len(ims) >= 1:
            repo_name = [im['RepoTags'][0] for im in client.images()][0]

    assert repo_name, 'No image given or found locally.'

    # get image if not available locally
    im_names = [im['RepoTags'][0] for im in client.images()] # all the images in the host (first tag)

    if (not any([repo_name in imname for imname in im_names])) and client.search(repo_name): # not found locally and found remote
        print('Image {} not found locally. Pulling from docker hub.'.format(repo_name))
        for line in client.pull(repo_name, tag, stream=True):
            print(line.decode())