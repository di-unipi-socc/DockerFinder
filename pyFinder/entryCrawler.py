from pyfinder import Crawler
from docopt import docopt
import time


__doc__= """Crawler

Usage:
  entryScanner.py crawl  [--rmq=<127.0.0.1>] [--queue=<dofinder>] [--fp=<1>] [--ps=<10>]  [--mi=<100>]
  entryScanner.py (-h | --help)
  entryScanner.py --version

Options:
  -h --help     Show this screen.
  --rmq=RabbitMQ       Hostname/Ip of the host running the rabbitMQ server [default: 127.0.0.1]
  --queue=QUEUE        Queue is the name of the queue of rabbitMQ [default: dofinder]
  --fp=FROM_PAGE      From Page: starting page crawled from the docker hub [default: 1].
  --ps=PAGE_SIZE      number of images in a single page [default: 10].
  --mi=MAX_PAGE       Max number of images to be craw from the docker hub [default: 100].
  --version     Show version.
"""

if __name__ == '__main__':

    args = docopt(__doc__, version='Crawler 0.0.1')
    print(args)
    if args['crawl']:
        crawler = Crawler(host_rabbit=args['--rmq'], queue_rabbit=args['--queue'])
        crawler.crawl(max_images=int(args['--mi']), page_size=int(args['--ps']), from_page=int(args['--fp']))
