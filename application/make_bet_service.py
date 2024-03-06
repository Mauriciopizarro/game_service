from dependency_injector.wiring import Provide, inject
from domain.interfaces.game_repository import GameRepository
from infrastructure.injector import Injector


class MakeBetService:

    @inject
    def __init__(self, game_repository: GameRepository = Provide[Injector.game_repo]):
        self.game_repository = game_repository

    def place_bet(self, game_id, player_id, bet_amount):
        game = self.game_repository.get(game_id)
        game.place_bet_to_current_player(player_id, bet_amount)
        self.game_repository.update(game)
