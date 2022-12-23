from abc import ABC, abstractmethod
from domain.game import Game


class GameRepository(ABC):

    @abstractmethod
    def get(self, game_id: int) -> Game:
        pass

    @abstractmethod
    def get_by_user_id(self, user_id: str) -> dict:
        pass

    @abstractmethod
    def save(self, game: Game) -> Game:
        pass

    @abstractmethod
    def update(self, game: Game) -> Game:
        pass
