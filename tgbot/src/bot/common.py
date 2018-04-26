import logging
import sys
import os

import settings


def mini_log(name, level=None, log_namespace=settings.PROGRAM_NAME):

    fullname = log_namespace + '.' + name

    log_level = level or settings.BASE_LOGLEVEL

    log_format = '(%(filename)15.15s:%(lineno)04d|%(threadName)8.12s): '
    log_format = '%(asctime)s.%(msecs)03d ' + log_format
    log_format += "%(levelname)s: %(message)s"

    date_format = "%Y.%m.%d %H:%M:%S"

    log = logging.getLogger(log_namespace)
    log.setLevel(log_level)
    log.propagate = False

    if not log.handlers:
        # stream
        stream_handler = logging.StreamHandler(sys.stdout)
        stream_handler.setFormatter(logging.Formatter(log_format, date_format))
        stream_handler.setLevel(log_level)
        log.addHandler(stream_handler)

        # file
        file_handler = logging.FileHandler(
            os.path.join(settings.LOGS_DIR, 'debug.log'))
        file_handler.setFormatter(logging.Formatter(log_format, date_format))
        file_handler.setLevel(log_level)
        log.addHandler(file_handler)

    return logging.getLogger(fullname)
