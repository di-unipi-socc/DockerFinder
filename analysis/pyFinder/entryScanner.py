from pyfinder import Scanner
from pyfinder.model.image import Image
from docopt import docopt
import time
from os import path
import logging.config
__doc__= """Scanner.

Usage:
    Scanner.py run [--amqp-url=<amqp://guest:guest@rabbitmq:5672>] [--ex=<dofinder>] [--queue=<images>] [--key=<images.scan>] [--images-url=<http://images_server:3000/api/images>] [--software-url=<http://software_server:3001/api/software>] [--hub-url=<https://hub.docker.com/>] [--rmi]
    Scanner.py scan <name> [--images-url=<http:://images_server:3000/api/images>] [--software-url=<http://software_server:3001/api/software>]
    Scanner.py exec <name> --p=<program>  --opt=<option>  --regex=<regex>
    Scanner.py (-h | --help)
    Scanner.py --version

Options:
  -h --help             Show this screen.
  --amqp-url=AMQP-URL   url of the rabbitMQ  server             [default: amqp://guest:guest@rabbitmq:5672]
  --ex=EXCHANGE         The exchange name of the rabbitMQ       [default: dofinder]
  --queue==QUEUE        Queue name of the rabbitMQ server       [default: images]
  --key=KEY             Routing key used by the rabbitMQ server [default: images.scan]
  --images-url=IMAGES_URL      The url of the images service    [default: http://images_server:3000/api/images/]
  --software-url=SOFTWARE-URL  THe url of the software service  [default: http://software_server:3001/api/software/]
  --hub-url=HUB-URL            The url of the DockerHub          [default: https://hub.docker.com]
  --rmi                 If True remove the images after the scan.
  --p=PROGRAM           The program name to pass to the container.
  --opt=OPTION          Option of the command to run in the contianer
  --regex=REGEX          Regular expression used to exctarct info of PROGRAM OPTION
  --version             Show version.
"""

# interactive mode for scanner
# docker run -it --net=core-net --entrypoint=/bin/sh dofinder/scanner:latest

if __name__ == '__main__':
    args = docopt(__doc__, version='Scanner 0.0.1')
    #print(args)
    log_file_path = path.dirname(path.abspath(__file__))+ '/pyfinder/resources/logging.conf'
    logging.config.fileConfig(log_file_path)
    logger = logging.getLogger()
    logger.info("Logging conf: "+ log_file_path)

    scanner = Scanner(amqp_url=args['--amqp-url'], exchange=args['--ex'], queue=args['--queue'], route_key=args['--key'],
                      images_url=args['--images-url'],
                      software_url=args['--software-url'],
                      hub_url=args['--hub-url'],
                      rmi=args['--rmi'])

    if args['scan']:
        image_name = args['<name>']
        #tag = args['--tag']
        # image_name = repository:tag
        image = Image({"name":image_name})
        #dict_image = scanner.scan(image)
        scanner.process_repo_name(image)
        #for sw_json in dict_image['softwares']: # list of json software :{"software": <name>,  "ver":<version>}
        #     print(sw_json['software'] + " " + sw_json['ver'])
        #print(str(len(dict_image['softwares']))+" software found in "+ image_name)
        # print(dict_image['distro'] + " distribution of " + image_name)

    if args['exec']:
        print(args)
        out = scanner.version_from_regex(args['<name>'],args['--p'],args['--opt'], args['--regex'])
        print(out)

    if args['run']:
        scanner.run()

    # if args['pull'] and args['officials']:
    #     scanner.pull_officials()
