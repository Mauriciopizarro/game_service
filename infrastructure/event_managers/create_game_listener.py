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
        logger.info('Received message')
        create_game_service = CreateGameService()
        event = json.loads(body)
        # Aca se debe llamar al game service mediante una request http
        # Ya que al llamar al metodo create_game estamos haciendolo en el contenedor del consumer
        # TODO crear un endpoint del ms game_service que llame al metodo create_game
        create_game_service.create_game(players=event["players"], game_id=event["id"])
        logger.info('Message consumed')
