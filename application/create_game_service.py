import random
from application.exceptions import EmptyPlayersList, IncorrectGameID
from domain.card import As, LetterCard, NumberCard
from domain.game import Game
from domain.player import Player
from domain.interfaces.game_repository import GameRepository


class CreateGameService:

    def __init__(self, game_repository: GameRepository):
        self.game_repository = game_repository

    def create_game(self, players, game_id):
        if not players:
            raise EmptyPlayersList("Empty players_list, please check if the event has sent correctly the message")
        if not game_id:
            raise IncorrectGameID("Empty game_id, please check if the event has sent correctly the message")
        game = Game(deck=self.create_deck(), game_status="pending_bet", game_id=game_id)
        player_list = []
        for player in players:
            player = Player(cards=[], name=player.name, player_id=player.user_id, status="waiting_turn", bet_amount=0)
            player_list.append(player)
        game.add_players(player_list)
        game.deal_initial_cards()
        return self.game_repository.save(game)

    @staticmethod
    def create_deck():
        cards = [
            As(),  # As
            As(),  # As
            As(),  # As
            As(),  # As
            LetterCard('J'),  # J
            LetterCard('J'),  # J
            LetterCard('J'),  # J
            LetterCard('J'),  # J
            LetterCard('Q'),  # Q
            LetterCard('Q'),  # Q
            LetterCard('Q'),  # Q
            LetterCard('Q'),  # Q
            LetterCard('K'),  # K
            LetterCard('K'),  # K
            LetterCard('K'),  # K
            LetterCard('K'),  # K
            NumberCard(2),
            NumberCard(2),
            NumberCard(2),
            NumberCard(2),
            NumberCard(3),
            NumberCard(3),
            NumberCard(3),
            NumberCard(3),
            NumberCard(4),
            NumberCard(4),
            NumberCard(4),
            NumberCard(4),
            NumberCard(5),
            NumberCard(5),
            NumberCard(5),
            NumberCard(5),
            NumberCard(6),
            NumberCard(6),
            NumberCard(6),
            NumberCard(6),
            NumberCard(7),
            NumberCard(7),
            NumberCard(7),
            NumberCard(7),
            NumberCard(8),
            NumberCard(8),
            NumberCard(8),
            NumberCard(8),
            NumberCard(9),
            NumberCard(9),
            NumberCard(9),
            NumberCard(9),
            NumberCard(10),
            NumberCard(10),
            NumberCard(10),
            NumberCard(10),
        ]
        random.shuffle(cards)
        return cards
