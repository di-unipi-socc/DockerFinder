from pyfinder import Crawler
from pyfinder import Tester
from docopt import docopt
from os import path
import logging.config

 # policy = 'stars',
 # min_stars = 0,
 # min_pulls = 0,
 # only_automated = False,
 # only_official = False
__doc__= """Crawler

Usage:
  Crawler.py crawl  [--save-url=</data/crawler/lasturl.txt>] [--amqp-url=<amqp://guest:guest@rabbitmq:5672>] [--hub-url=<https://hub.docker.com>] [--images-url=<http://images_server:3000/api/images>] [--queue=<dofinder>] [--ex=<dofinder>] [--key=<images.scan>] [--random=<False>] [--force-page=<False>] [--fp=<1>] [--ps=<10>]  [--si=<100>]
  Crawler.py (-h | --help)
  Crawler.py --version

Options:
  -h --help     Show this screen.
  --amqp-url=AMQP_URL  Complete amqp url of the rabbitMQ server     [default: amqp://guest:guest@rabbitmq:5672]
  --save-url==FILE_SAVE File where the crawler save the last url crawled [default:/data/crawler/lasturl.txt]
  --queue=QUEUE        Queue is the name of the queue of rabbitMQ   [default: images]
  --images-url=IMAGES_URL      The url of the images service        [default: http://127.0.0.1:3000/api/images]
  --hub-url=HUB-URL            The url of the DockerHub             [default: https://hub.docker.com]
  --ex=EXCHANGE        Exchange name in the rabbitMQ.               [default: dofinder]
  --key=KEY            Key routing for the rabbitMQ.                [default: images.scan]
  --fp=FROM_PAGE      From Page: starting page crawled from the docker hub [default: 1].
  --ps=PAGE_SIZE      number of images in a single page                    [default: 100].
  --si=SAMPLED_IMAGES Number of images sampled from Docker hub      [default: None].
  --random=RANDOM     If True the sampled images are random dampled [default: True]
  --force-page=FORCE PAGE   If True the crawler start from the from_image, otherwise take the last url [default: False]
  --version     Show version.
"""

if __name__ == '__main__':
    args = docopt(__doc__, version='Crawler 0.0.1')

    log_file_path = path.dirname(path.abspath(__file__))+ '/pyfinder/resources/logging.conf'
    logging.config.fileConfig(log_file_path)
    logger = logging.getLogger()
    logger.info("Logging conf: "+ log_file_path)

    if args['crawl']:
        policy = 'stars',
        # min_stars = 0,
        # min_pulls = 0,
        # only_automated = False,
        # only_official = False
        crawler = Crawler(amqp_url=args['--amqp-url'],
                          queue=args['--queue'],
                          images_url=args['--images-url'],
                          hub_url=args['--hub-url'],
                          exchange=args['--ex'],
                          route_key=args['--key'],
                          path_last_url=args['--save-url'],
                          policy="stars",
                          min_pulls=100,
                          min_stars = 3,
                          only_official = False,
                          only_official = False
                          )
        crawler.run(num_samples = None if args['--si'] == "None" else int(args['--si']),
                    page_size=None if args['--ps'] == "None"  else int(args['--ps']),
                    from_page=None if args['--fp'] == "None"  else int(args['--fp']),
                    at_random=True if args['--random'] == "True" else False,
                    force_from_page= True if args['--force-page'] =="True" else False
                    )

    if args['test']:
        tester = Tester(path_file_images=args['--pf'])
        if args['build']:
            tester.build_test(num_images_test=int(args['--ni']), from_page=int(args['--fp']))

        if args['send']:
            tester.push_test(amqp_url=args['--amqp-url'], exchange=args['--ex'], queue=args['--queue'],
                             route_key=args['--key'])
