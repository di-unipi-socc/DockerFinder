from pyfinder import Scanner
from docopt import docopt
import time
__doc__= """Scanner.

Usage:
  entryScanner.py run [--rmi] [--hr=<127.0.0.1>] [--qr=<dofinder>] [--hi=<images_server>] [--pi=<3000>] [--bi=</api/images>]
  entryScanner.py scan <name> [--tag=<latest>]
  entryScanner.py pull officials
  entryScanner.py (-h | --help)
  entryScanner.py --version

Options:
  -h --help             Show this screen.
  --hr=HOST_RABBIT      Host of the rabbitMQ  running server [default: 127.0.0.1]
  --qr=QUEUE_RABBIT     Name of the queue where to get info from the rabbitMQ [default: dofinder]
  --hi=HOST_IMAGES      Host of the images service [default: images_server]
  --pi=PORT_IMAGES      Port of the images service [default: 3000]
  --bi=BASE_IMAGES      Base path of the images service. [default: /api/images]
  -rmi                  Remove the images after the scan.
  --tag=TAG             TAG  of the image to scan [default: latest]
  --version             Show version.
"""

# interactive mode for scanner
#docker run -it --net=core-net --entrypoint=/bin/sh dofinder/scanner:latest

if __name__ == '__main__':
    args = docopt(__doc__, version='Scanner 0.0.1')
    # print(args)
    scanner = Scanner(host_rabbit=args['--hr'], queue_rabbit=args['--qr'],
                      host_images=args['--hi'],
                      port_images=args['--pi'],
                      path_images=args['--bi'],
                      rmi=int(args['--rmi']))

    if args['scan']:
        image_name = args['<name>']
        tag = args['--tag']
        scanner.scan(image_name, tag=tag)

    if args['run']:
        scanner.run()

    if args['pull'] and args['officials']:
        scanner.pull_officials()

    #port_rabbit = 5672, host_rabbit = '172.17.0.2', url_api = "127.0.0.1:8000/api/images"
    #port_rabbit=5672, host_rabbit='172.17.0.2', url_imagesservice="127.0.0.1:8000/api/images"
