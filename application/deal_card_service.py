from infrastructure.http_clients.wallet_service_http_client import WalletServiceHttpClient
from domain.interfaces.game_repository import GameRepository
from config import settings


class DealCardService:

    def __init__(self, game_repository: GameRepository, wallet_service_http_client: WalletServiceHttpClient):
        self.game_repository = game_repository
        self.wallet_service_http_client = wallet_service_http_client

    def deal_card(self, player_id, game_id):
        game = self.game_repository.get(game_id)
        game.deal_card_to_current_turn_player(player_id)
        self.game_repository.update(game)
        #TODO
        #this pay bets logic should be in a bounded context specific
        if game.game_status == 'finished':
            for player in game.turn_order:
                if player.name != "Croupier":
                    if player.status == 'winner':
                        message = {
                            "user_id": player.player_id,
                            "amount": player.get_bet() * int(settings.MULTIPLY_BET_AMOUNT)
                        }
                        self.wallet_service_http_client.set_money(user_id=message["user_id"], amount=message["amount"])
