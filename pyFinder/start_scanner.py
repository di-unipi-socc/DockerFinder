from pyfinder import Scanner
from docopt import docopt
import time
__doc__= """Scanner.

Usage:
  start_scanner.py run
  start_scanner.py scan <name>  [--tag=<latest>]
  start_scanner.py ship shoot <x> <y>
  start_scanner.py mine (set|remove) <x> <y> [--moored | --drifting]
  start_scanner.py (-h | --help)
  start_scanner.py --version

Options:
  -h --help     Show this screen.
  --tag=TAG     The TAG is the tag of the image to scan [default: latest]
  --version     Show version.
  --speed=<kn>  Speed in knots [default: 10].
  --moored      Moored (anchored) mine.
  --drifting    Drifting mine.
"""

if __name__ == '__main__':
    time.sleep(7)
    print("waitied 5 ec")
    #port_rabbit=5672, host_rabbit='172.17.0.2', url_imagesservice
    scanner = Scanner(host_rabbit='rabbitmq', url_imagesservice='http://images_server:3000/api/images')
    args = docopt(__doc__, version='Scanner 0.0.1')
    #print(args)
    if args['scan']:
        image_name = args['<name>']
        tag = tag=args['--tag']
        scanner.scan(image_name, tag=tag)
    if args['run']:
        scanner.run()

    #port_rabbit = 5672, host_rabbit = '172.17.0.2', url_api = "127.0.0.1:8000/api/images"
    #port_rabbit=5672, host_rabbit='172.17.0.2', url_imagesservice="127.0.0.1:8000/api/images"
