from infrastructure.event_managers.rabbit_consumer import RabbitConsumer
from infrastructure.logging import LogConfig
from logging.config import dictConfig
import requests
import logging
import json

dictConfig(LogConfig().dict())
logger = logging.getLogger("blackjack")


class CreateGameListener(RabbitConsumer):

    topic = "game_started"

    def process_message(self, channel, method, properties, body):
        logger.info('Received message')
        event = json.loads(body)
        players = event["players"]
        game_id = event["id"]
        url = "http://game_service:5002/game/create"
        requests.post(url=url, json={
            "game_id": game_id,
            "players": players
        })
        logger.info('Message consumed')
