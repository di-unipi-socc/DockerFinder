import datetime
import time
import logging
import pickle


def string_to_date(string_date):
    return datetime.datetime(*time.strptime(string_date, "%Y-%m-%dT%H:%M:%S.%fZ")[:7])



def get_logger(name_class, level=logging.DEBUG):

    logger = logging.getLogger(name_class)
    # logging.basicConfig(level=logging.DEBUG)
    logger.setLevel(level)
    #print(name_class + ": " + level + " logging level setted")

    # create file handler which logs even debug messages

    # create console handler with a higher log level
    ch = logging.StreamHandler()
    ch.setLevel(level)

    # create formatter and add it to the handlers
    LOG_FORMAT = ('%(asctime)s %(levelname)s  %(funcName) -5s %(lineno) -5d: %(message)s')
    formatter = logging.Formatter(LOG_FORMAT, datefmt='%m/%d/%Y %I:%M:%S')

    ch.setFormatter(formatter)
    # add the stream handlers to the logger
    logger.addHandler(ch)

    assert isinstance(logger, logging.Logger)
    return logger
