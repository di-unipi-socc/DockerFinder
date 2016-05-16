import click
import os
import docker





'''
@click.command()
@click.argument('do', nargs=-1)
@click.option('--image', '-i', help='Image name in which to run do', default=None)
@click.option('--sharedir', '-s', help='Directory on host machine to mount to docker.', default=os.path.abspath(os.getcwd()))
@click.option('--display', '-d', help='Display variable to set for X11 forwarding.', default=None)
def dodo(do, image, sharedir, display):
    """ dodo (like sudo but for docker) runs argument in a docker image.
    do is the command to run in the image.
    image taken from (1) command-line, (2) "DODOIMAGE" environment variable, or (3) first built image.
    sharedir (e.g., to pass data to command) is mounted (default: current directory). empty string does no mounting.
    display is environment variable to set in docker image that allows X11 forwarding.
    """

    # try to set image three ways
    if not image:
        if 'DODOIMAGE' in os.environ:
            image = os.environ['DODOIMAGE']
        else:
            ims = client.images()
            if len(ims) >= 1:
                image = [im['RepoTags'][0] for im in client.images()][0]

    assert image, 'No image given or found locally.'

    # get image if not available locally
    imnames = [im['RepoTags'][0] for im in client.images()]
    if (not any([image in imname for imname in imnames])) and client.search(image):
        print('Image {} not found locally. Pulling from docker hub.'.format(image))
        client.pull(image)

    # mount directory in docker
    if sharedir:
        volumes = ['{}:/home'.format(sharedir)]
    else:
        volumes = []

    # set docker environment to display X11 locally
    if display:
        environment = ['DISPLAY={}'.format(display)]
    elif 'DODODISPLAY' in os.environ:
        environment = ['DISPLAY={}'.format(os.environ['DODODISPLAY'])]
    else:
        environment = []

    with Container(image, volumes=volumes, cleanup=True, environment=environment) as c:
        for output_line in c.run(do):
            print('{}:\t {}'.format(image, output_line.decode('utf-8')))
'''


