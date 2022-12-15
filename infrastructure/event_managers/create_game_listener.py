from application.create_game_service import CreateGameService
from infrastructure.event_managers.rabbit_consumer import RabbitConsumer
from logging.config import dictConfig
import logging
import json
from infrastructure.logging import LogConfig

dictConfig(LogConfig().dict())
logger = logging.getLogger("blackjack")


class CreateGameListener(RabbitConsumer):

    topic = "game_started"

    def process_message(self, channel, method, properties, body):
        create_game_service = CreateGameService()
        logger.info('Received message')
        event = json.loads(body)
        create_game_service.create_game(players=event["players"], game_id=event["id"])
        logger.info('Message consumed')
