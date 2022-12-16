from dependency_injector.wiring import Provide, inject
from infrastructure.injector import Injector
from domain.interfaces.game_repository import GameRepository


class HistoryGamesService:

    @inject
    def __init__(self, game_repository: GameRepository = Provide[Injector.game_repo]):
        self.game_repository = game_repository

    def get_history(self, user_id):
        games_played = self.game_repository.get_games_for_a_user(user_id)
        # Remove and reformat the keys for the response
        for results in games_played:
            results.pop("deck")
            results.pop("turn_position")
            results["game_id"] = str(results.get("_id").get("$oid"))
            results["status"] = results.get("game_status")
            for player in results.get("turn_order"):
                if player.get("player_id") == user_id:
                    results["player_status"] = player.get("status")
            results.pop("_id")
            results.pop("game_status")
            results.pop("turn_order")
        return games_played
