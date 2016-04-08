#from sidomo import Container
from _ast import Add

from docker import Client

cli = Client(base_url='unix://var/run/docker.sock')

"""
# -v mount a volume, -w set working directory on container
# docker run -v `pwd`:/path/container -w /path/container -i -t ubuntu

container = cli.create_container(
    'ubuntu', command='echo ciao', working_dir="/mnt/vol2",tty=True,stdin_open=True, volumes=['/mnt/vol1', '/mnt/vol2'],
    host_config=cli.create_host_config(binds={
        '/home/dido-ubuntu/': {
            'bind': '/mnt/vol2',
            'mode': 'rw',
        },
        '/var/www': {
            'bind': '/mnt/vol1',
            'mode': 'ro',
        }
    })
)
"""

cli.create_container('ubuntu', command='echo ciao',stdin_open=True,tty=True)



