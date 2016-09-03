#  -*- coding: utf-8 -*-
import logging
FLIE_NAME = "log.txt"


def set_log(content, level):
    """
    write log to file
    :param content:log content
    :param level:log level
    """
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s:%(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                        datefmt='%a, %d %b %Y %H:%M:%S',
                        filename=FLIE_NAME,
                        filemode='w')
    if level == 0:
        logging.info(content)
    elif level == 1:
        logging.debug(content)
    elif level == 2:
        logging.error(content)