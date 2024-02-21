from abc import abstractmethod
import pika
from logging.config import dictConfig
import logging
from infrastructure.logging import LogConfig
from urllib.parse import urlparse
from config import settings

dictConfig(LogConfig().dict())
logger = logging.getLogger("blackjack")


class RabbitConsumer:

    topic = None

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
        self.channel.basic_consume(queue=self.topic, on_message_callback=self.process_message, auto_ack=True)
        logger.info(f'Established async listener in topic {self.topic}')
        self.channel.start_consuming()

    @abstractmethod
    def process_message(self, channel, method, properties, body):
        pass
