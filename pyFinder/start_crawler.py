from pyfinder import Crawler
from docopt import docopt
import time


__doc__= """Crawler

Usage:
  start_scanner.py run
  start_scanner.py crawl   [--tag=<latest>]
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
    time.sleep(10)
    print("waited 5 sec::")
    crawler = Crawler(host_rabbit="rabbitmq")
    args = docopt(__doc__, version='Crawler 0.0.1')
    crawler.crawl()
    #print(args)
    if args['crawl']:
        crawler.crawl()
    #port_rabbit = 5672, host_rabbit = '172.17.0.2', url_api = "127.0.0.1:8000/api/images"
    #port_rabbit=5672, host_rabbit='172.17.0.2', url_imagesservice="127.0.0.1:8000/api/images"
