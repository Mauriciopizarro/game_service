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

    def get_statuses(self, game_ids) -> dict:
        """Devuelve {game_id: status_game}. Default: N lecturas (compatible).

        Los repositorios que soportan queries por lote (mongo `$in`) deberían
        overridear este método para evitar llamadas por elemento.
        """
        statuses = {}
        for game_id in game_ids:
            game = self.get(game_id)
            if game:
                statuses[str(game_id)] = game.game_status
        return statuses
