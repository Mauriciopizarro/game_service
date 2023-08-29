from abc import abstractmethod
import pika
from logging.config import dictConfig
import logging
from infrastructure.logging import LogConfig

dictConfig(LogConfig().dict())
logger = logging.getLogger("blackjack")


class RabbitConsumer:

    topic = None

    def __init__(self):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host="rabbitmq", heartbeat=9999, blocked_connection_timeout=300)
        )
        self.channel = self.connection.channel()
        self.channel.basic_consume(queue=self.topic, on_message_callback=self.process_message, auto_ack=True)
        logger.info(f'Established async listener in topic {self.topic}')
        self.channel.start_consuming()

    @abstractmethod
    def process_message(self, channel, method, properties, body):
        pass
