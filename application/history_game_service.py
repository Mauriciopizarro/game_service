from domain.interfaces.game_repository import GameRepository


class HistoryGamesService:

    def __init__(self, game_repository: GameRepository):
        self.game_repository = game_repository

    def get_history(self, user_id):
        games_played = self.game_repository.get_by_user_id(user_id)
        return games_played
