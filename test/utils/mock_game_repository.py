from domain.game import Game
from domain.interfaces.game_repository import GameRepository


class MockGameRepository(GameRepository):

    def __init__(self, game=None):
        self.game = game

    def get(self, game_id: int) -> Game:
        return self.game

    def get_by_user_id(self, user_id: str) -> dict:
        pass

    def save(self, game: Game) -> Game:
        return game

    def update(self, game: Game) -> Game:
        return self.game