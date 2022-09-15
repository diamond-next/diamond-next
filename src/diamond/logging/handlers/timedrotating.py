# coding=utf-8

import sys
from logging.handlers import TimedRotatingFileHandler as TRFH


class TimedRotatingFileHandler(TRFH):
    def flush(self):
        try:
            super(TimedRotatingFileHandler, self).flush()
        except IOError:
            sys.stderr.write('TimedRotatingFileHandler received a IOError!')
            sys.stderr.flush()
