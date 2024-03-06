import pika
from config import settings
from logging.config import dictConfig
import logging
from infrastructure.logging import LogConfig

dictConfig(LogConfig().dict())
logger = logging.getLogger("blackjack")


class RabbitConnection:

    instance = None

    def __init__(self):
        credentials = pika.PlainCredentials(settings.RABBIT_USERNAME, settings.RABBIT_PASSWORD)
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=settings.RABBIT_HOST,
                                      heartbeat=9999,
                                      blocked_connection_timeout=300,
                                      credentials=credentials,
                                      virtual_host=settings.RABBIT_VHOST)
        )
        self.channel = self.connection.channel()
        logger.warning('Rabbit connection initialized')

    @classmethod
    def get_channel(cls):
        instance = cls.init_connection()
        return instance.channel

    @classmethod
    def get_connection(cls):
        instance = cls.init_connection()
        return instance.connection

    @classmethod
    def init_connection(cls):
        if not cls.instance:
            cls.instance = cls()
        return cls.instance

    @staticmethod
    def declare_queues(channel, queues):
        for queue in queues:
            channel.queue_declare(queue)
