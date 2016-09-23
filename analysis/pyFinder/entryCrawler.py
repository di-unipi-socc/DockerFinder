from pyfinder import Crawler
from pyfinder import Tester
from docopt import docopt

__doc__= """Crawler

Usage:
  Crawler.py crawl  [--amqp-url=<amqp://guest:guest@rabbitmq:5672>] [--queue=<dofinder>] [--ex=<dofinder>] [--key=<images.scan>]  [--fp=<1>] [--ps=<10>]  [--mi=<100>]
  Crawler.py (-h | --help)
  Crawler.py --version

Options:
  -h --help     Show this screen.
  --amqp_url=AMQP_URL  Complete amqp url of the rabbitMQ server     [default: amqp://guest:guest@rabbitmq:5672]
  --queue=QUEUE        Queue is the name of the queue of rabbitMQ   [default: images]
  --ex=EXCHANGE        Exchange name in the rabbitMQ.               [default: dofinder]
  --key=KEY            Key routing for the rabbitMQ.                [default: images.scan]
  --fp=FROM_PAGE      From Page: starting page crawled from the docker hub [default: 1].
  --ps=PAGE_SIZE      number of images in a single page [default: 10].
  --mi=MAX_PAGE       Max number of images to be crawled from the docker hub [default: None].
  --version     Show version.
"""

if __name__ == '__main__':
    args = docopt(__doc__, version='Crawler 0.0.1')

    if args['crawl']:
        crawler = Crawler(amqp_url=args['--amqp-url'],
                          queue=args['--queue'],
                          exchange=args['--ex'],
                          route_key=args['--key'])
        crawler.run(max_images=None if args['--mi'] == "None" else int(args['--mi']),
                    page_size=int(args['--ps']),
                    from_page=int(args['--fp']))

    if args['test']:
        tester = Tester(path_file_images=args['--pf'])
        if args['build']:
            tester.build_test(num_images_test=int(args['--ni']), from_page=int(args['--fp']))

        if args['send']:
            tester.push_test(amqp_url=args['--amqp-url'], exchange=args['--ex'], queue=args['--queue'],
                             route_key=args['--key'])

