import logging
logger = logging.getLogger("slave." + __name__)


def sum(a, b):
    s = a + b
    logger.debug("received params %s, %s; sum %s", a, b, s)
    return s


def mult(a, b):
    m = a * b
    logger.debug("received params %s, %s; multiply %s", a, b, m)
    return m
