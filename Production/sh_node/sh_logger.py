import os
import logging

import sys

LOG_PATH = 'logs'
LOG_FILE = 'text.txt'


def get_logger(name):
    i_logger = logging.getLogger(name)
    if os.path.exists(LOG_PATH):
        pass
    else:
        os.mkdir(LOG_PATH)

    formatter = logging.Formatter('%(asctime)s %(levelname)-8s: %(message)s')

    file_handler = logging.FileHandler("%s/%s" % (LOG_PATH, LOG_FILE))
    file_handler.setFormatter(formatter)  

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.formatter = formatter
   
    i_logger.addHandler(file_handler)
    i_logger.addHandler(console_handler)
   
    i_logger.setLevel(logging.DEBUG)
    return i_logger


if __name__ == '__main__':
    logger = get_logger(__name__)
    logger.debug('test')
