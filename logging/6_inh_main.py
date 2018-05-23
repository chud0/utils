import sys
import logging

# it's ugly, but i don't now how import module with name in number on first position
log_dict_conf = __import__("4_dictConfig")
slave = __import__("6_inh_slave")

logger = logging.getLogger("slave." + __name__)
logger.debug("logger with name: %s created", logger.name)


def simple_func(a, b, c):
    s = slave.sum(a, b)
    m = slave.mult(s, c)
    logger.debug("received params %s, %s, %s; return %s", a, b, c, m)
    return m


if __name__ == "__main__":
    args = sys.argv[1:4]
    if len(args) == 3:
        logger.debug("received params from sys.argv")
        args = list(map(int, args))
    else:
        args = [4, 5, 6]
        logger.debug("load default params")
    logger.info("received params %s, %s, %s", *args)
    logger.info(simple_func(*args))
