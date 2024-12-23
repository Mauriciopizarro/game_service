import json
import pika
import uuid
from domain.interfaces.publisher import Publisher
from infrastructure.event_managers.rabbit_connection import RabbitConnection
from logging.config import dictConfig
import logging
from infrastructure.logging import LogConfig
from datadog import statsd
from infrastructure.datadog import configure_datadog

dictConfig(LogConfig().dict())
logger = logging.getLogger("blackjack")

# Configure DataDog
configure_datadog()


class RabbitPublisher(Publisher):

    def send_message(self, message: dict, topic: str):
        """Method to publish message to RabbitMQ"""

    try:
        publish_queue_name = topic
        channel = RabbitConnection.get_channel()
        channel.basic_publish(
            exchange='',
            routing_key=publish_queue_name,
            properties=pika.BasicProperties(
                correlation_id=str(uuid.uuid4())
            ),
            body=json.dumps(message)
        )
        logger.info('Message published')

        # Métrica para DataDog
        statsd.increment('rabbitmq.messages_published', tags=[f"topic:{topic}"])
        statsd.event(
            title="Message Published",
            text=f"Message published to topic {topic}",
            tags=["rabbitmq", f"topic:{topic}"]
        )

    except Exception as e:
        logger.error(f"Error publishing message: {e}")
        statsd.increment('rabbitmq.publish_errors', tags=[f"topic:{topic}"])
