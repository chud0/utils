import logging
import logging.handlers
import pika
import pika.exceptions
import os


rmq_logger = logging.getLogger("rmq_debug")
rmq_logger.setLevel(logging.DEBUG)
rmq_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
rmq_cons_handler = logging.StreamHandler()
rmq_cons_handler.setFormatter(rmq_formatter)
rmq_logger.addHandler(rmq_cons_handler)


class RabbitMQHandler(logging.Handler):

    def __init__(self, host, port, login, password, exchange, routing_key):
        credentials = pika.PlainCredentials(login, password)
        self.connection_params = pika.ConnectionParameters(host, port, '/', credentials, heartbeat=5)
        self.exchange = exchange
        self.routing_key = routing_key

        self.connection = None
        self.channel = None

        super().__init__()

        rmq_logger.debug("inital handler")

    def check_connection(self):
        rmq_logger.debug("checked conection")
        rmq_logger.debug("conection is %s", bool(self.connection and self.connection.is_open))
        return self.connection and self.connection.is_open

    def open_connection(self):
        rmq_logger.debug("try open connection")

        try:
            self.connection = pika.BlockingConnection(self.connection_params)
            self.channel = self.connection.channel()
        except pika.exceptions.ConnectionClosed as e:
            log_record = logging.LogRecord(self.__class__.__name__, logging.WARNING, os.getcwd(), "40",
                                           "Can't connect to RMQ server", "", "")
            self.handleError(log_record)
            raise e

    def publish_record(self, log_record):
        try:
            self.channel.publish(exchange=self.exchange, body=self.format(log_record),
                                 routing_key="{}.{}".format(self.routing_key, log_record.levelname),)
        except pika.exceptions.UnroutableError:
            rmq_logger.debug("UnroutableError")
            self.handleError(log_record)

    def emit(self, log_record):
        rmq_logger.debug("emit called")
        if not self.check_connection():
            self.open_connection()

        try:
            self.publish_record(log_record)
        except pika.exceptions.ConnectionClosed:
            rmq_logger.debug("connection closed")
            rmq_logger.debug("connection.is_open say %s", self.connection.is_open)
            self.open_connection()
            self.publish_record(log_record)

        rmq_logger.debug("log record with name %s, level %s", log_record.name, log_record.levelname)

    def close_connection(self):
        rmq_logger.debug("closed connection")

        if self.check_connection():
            self.channel.close()
            self.connection.close()

        self.connection, self.channel = None, None

    def close(self):
        self.close_connection()

        super().close()


if __name__ == "__main__":
    logger = logging.getLogger("rmq")

    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

    cons_handler = logging.StreamHandler()
    cons_handler.setFormatter(formatter)

    handler = RabbitMQHandler("host", "port", "login", "password", "exchange_name", "routing_key")
    handler.setFormatter(formatter)
    handler.setLevel(logging.DEBUG)

    logger.addHandler(handler)
    logger.addHandler(cons_handler)

    logger.setLevel(logging.DEBUG)

    logger.info("Start logging")

    import time
    import random

    while True:
        sleep_in_sec = random.randrange(20)
        logger.info("I sleep %s sec", sleep_in_sec)
        time.sleep(sleep_in_sec)
