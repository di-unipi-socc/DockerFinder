from pyfinder.tester import Tester

from docopt import docopt

__doc__= """Tester

Usage:
  Tester.py build [--ni=<100>] [--fp=<1>] [--pf=<images.test>]
  Tester.py send  [--amqp-url=<amqp://guest:guest@rabbitmq:5672>] [--ex=<dofinder>] [--key=<images.test>] [--queue=<test>]  [--pf=<images.test>]
  Tester.py pull officials
  Tester.py rmi
  Tester.py (-h | --help)
  Tester.py --version

Options:
  -h --help     Show this screen.
  --amqp_url=AMQP_URL  Complete amqp url of the rabbitMQ server     [default: amqp://guest:guest@rabbitmq:5672]
  --queue=QUEUE        Queue is the name of the queue of rabbitMQ   [default: test]
  --ex=EXCHANGE        Exchange name in the rabbitMQ.               [default: dofinder]
  --key=KEY            Key routing for the rabbitMQ.                [default: images.test]
  --fp=FROM_PAGE      From Page: starting page crawled from the docker hub [default: 1].
  --ni=NUMBER_IMAGES  Number of images to crawl in order to run the test [default: 100].
  --pf=PATH_FILE      Path of the file containing the set of images to test [default: images.test]
  --version     Show version.
"""

if __name__ == '__main__':
    args = docopt(__doc__, version='Tester 0.0.1')
    tester = Tester(path_file_images=args['--pf'])
    if args['build']:
        tester.build_test(num_images_test=int(args['--ni']), from_page=int(args['--fp']))

    if args['send']:
        tester.push_test(amqp_url=args['--amqp-url'], exchange=args['--ex'], queue=args['--queue'],
                         route_key=args['--key'])

    if args['pull'] and args['officials']:
        tester.pull_officials()

    if args['rmi']:
        tester.remove_no_officials()
