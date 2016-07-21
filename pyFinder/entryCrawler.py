from pyfinder import Crawler
from pyfinder import build_test
from docopt import docopt

__doc__= """Crawler

Usage:
  Crawler.py crawl  [--rmq=<127.0.0.1>] [--queue=<dofinder>] [--fp=<1>] [--ps=<10>]  [--mi=<100>]
  Crawler.py build test [--ni=<100>] [--pf=<images.test>]
  Crawler.py run test   [--rmq=<127.0.0.1>]  [--queue=<test>]  [--pf=<images.test>]
  Crawler.py (-h | --help)
  Crawler.py --version

Options:
  -h --help     Show this screen.
  --rmq=RabbitMQ       Hostname/Ip of the host running the rabbitMQ server [default: 127.0.0.1]
  --queue=QUEUE        Queue is the name of the queue of rabbitMQ [default: dofinder]
  --fp=FROM_PAGE      From Page: starting page crawled from the docker hub [default: 1].
  --ps=PAGE_SIZE      number of images in a single page [default: 10].
  --mi=MAX_PAGE       Max number of images to be craw from the docker hub [default: 100].
  --ni=NUMBER_IMAGES  Number of images to crawl in order to run the test [default: 100].
  --pf=PATH_FILE      Path of the file containing the set of images to test [default: images.test]
  --version     Show version.
"""

if __name__ == '__main__':
    args = docopt(__doc__, version='Crawler 0.0.1')
    # print(args)
    if args['crawl']:
        crawler = Crawler(host_rabbit=args['--rmq'], queue_rabbit=args['--queue'])
        crawler.crawl(max_images=int(args['--mi']), page_size=int(args['--ps']), from_page=int(args['--fp']))

    if args['build'] and args['test']:
        build_test(path_name_file=args['--pf'], num_images_test=int(args['--ni']))

    if args['run'] and args['test']:
        crawler = Crawler(host_rabbit=args['--rmq'], queue_rabbit=args['--queue'])
        crawler.run_test(path_name_file=args['--pf'])

