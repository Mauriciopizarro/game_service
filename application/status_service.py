from domain.interfaces.game_repository import GameRepository


class StatusService:

    def __init__(self, game_repository: GameRepository):
        self.game_repository = game_repository

    def players_status(self, game_id):
        game = self.game_repository.get(game_id)
        return game.get_status()
