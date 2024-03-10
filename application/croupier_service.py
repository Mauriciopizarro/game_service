from dependency_injector.wiring import Provide, inject
from infrastructure.injector import Injector
from domain.interfaces.game_repository import GameRepository
from domain.interfaces.publisher import Publisher
from logging.config import dictConfig
import logging
from infrastructure.logging import LogConfig

dictConfig(LogConfig().dict())
logger = logging.getLogger("blackjack")


class CroupierService:

    @inject
    def __init__(self, game_repository: GameRepository = Provide[Injector.game_repo],
                 publisher: Publisher = Provide[Injector.publisher]
                 ):
        self.publisher = publisher
        self.game_repository = game_repository

    def croupier_play(self, game_id):
        game = self.game_repository.get(game_id)
        game.croupier_play()
        for player in game.turn_order:
            if player.name != "Croupier":
                if player.status == 'winner':
                    message = {
                        "user_id": player.player_id,
                        "amount": player.get_bet() * 2
                    }
                    self.publisher.send_message(message=message, topic="set_money_account")
        self.game_repository.update(game)
