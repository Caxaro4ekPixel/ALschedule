import logging
import pprint
import sys

from loguru import logger

def pp(object):
    return pprint.pformat(object, indent=4, width=60, depth=4, compact=True, sort_dicts=True, underscore_numbers=True)


class InterceptHandler(logging.Handler):
    LEVELS_MAP = {
        logging.CRITICAL: "CRITICAL",
        logging.ERROR:    "ERROR",
        logging.WARNING:  "WARNING",
        logging.INFO:     "INFO",
        logging.DEBUG:    "DEBUG",
    }

    def _get_level(self, record):
        return self.LEVELS_MAP.get(record.levelno, record.levelno)

    def emit(self, record):
        logger_opt = logger.opt(depth=6, exception=record.exc_info)
        logger_opt.log(self._get_level(record), record.getMessage())


# noinspection PyArgumentList
def setup():
    logger.add(sys.stderr, format="{time} {level} {message}", filter="my_module", level="INFO")
    logging.basicConfig(handlers=[InterceptHandler()], level=logging.INFO)