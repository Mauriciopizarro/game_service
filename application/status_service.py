from domain.interfaces.game_repository import GameRepository


class StatusService:

    def __init__(self, game_repository: GameRepository):
        self.game_repository = game_repository

    def players_status(self, game_id):
        game = self.game_repository.get(game_id)
        return game.get_status()

    def statuses_by_ids(self, game_ids) -> dict:
        """Devuelve {game_id: status_game} para N ids en 1 sola consulta.

        El gateway lo usa para enriquecer el lobby: en vez de 1 llamada HTTP
        por partida (N+1, que satura el hosting free ante ráfagas), hace una
        única llamada batch.
        """
        return self.game_repository.get_statuses(game_ids)
