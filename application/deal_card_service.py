from domain.interfaces.publisher import Publisher
from domain.interfaces.game_repository import GameRepository
from config import settings


class DealCardService:

    def __init__(self, game_repository: GameRepository, publisher: Publisher):
        self.game_repository = game_repository
        self.publisher = publisher

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
                        self.publisher.send_message(message=message, topic="set_money_account")
