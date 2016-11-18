from pyfinder import Checker
from docopt import docopt
import time
__doc__= """Checker.

Usage:
  entryChecker.py run [--interval=<10>] [--path-logging=</data/crawler/log/stats.log>] [--key=<images.scan>] [--amqp-url=<amqp://guest:guest@rabbitmq:5672>] [--ex=<dofinder>] [--queue=<images>] [--images-url=<http://images_server:3000/api/images/>][--hub-url=<https://hub.docker.com/>]
  entryChecker.py (-h | --help)
  entryChecker.py --version

Options:
  -h --help             Show this screen.
  --amqp-url=AMQP-URL   url of the rabbitMQ  server             [default: amqp://guest:guest@rabbitmq:5672]
  --path-logging=PATH-LOGGING the path for storing              [default: /data/crawler/log/stats.log]
  --interval=interval   interval time in seconds between two consecutnve cheks [default:10]
  --ex=EXCHANGE         The exchange name of the rabbitMQ       [default: dofinder]
  --queue==QUEUE        Queue name of the rabbitMQ server       [default: images]
  --key==KEY            Routing key used by the rabbitMQ server [default: images.scan]
  --images-url=IMAGES_URL      The url of the images service    [default: http://127.0.0.1:3000/api/images/]
  --hub-url=HUB-URL            The url of the DockerHub         [default: https://hub.docker.com/]
  --version             Show version.
"""

# interactive mode for scanner
#docker run -it --net=core-net --entrypoint=/bin/sh dofinder/scanner:latest

if __name__ == '__main__':
    args = docopt(__doc__, version='Scanner 0.0.1')
    #print(args)
    checker = Checker(  amqp_url=args['--amqp-url'],
                        exchange=args['--ex'],
                        queue=args['--queue'],
                        route_key=args['--key'],
                        images_url=args['--images-url'],
                        hub_url=args['--hub-url'],
                        path_file_logging=args['--path-logging']
                        )

    if args['run']:
        checker.run(interval_next_check=int(args['--interval']))
