from domain.card import Card
from domain.player import Player, Croupier
from application.exceptions import GameFinishedError, GameStartedImpossibleBet
from typing import Optional, List
from pydantic import BaseModel
from logging.config import dictConfig
import logging
from infrastructure.logging import LogConfig

dictConfig(LogConfig().dict())
logger = logging.getLogger("blackjack")


class Game(BaseModel):
    turn_order: List[Player] = []
    deck: List[Card]
    game_status: str
    turn_position: int = 0
    game_id: Optional[str] = None

    @property
    def players(self):
        if len(self.turn_order) == 1:
            return []
        return self.turn_order[:-1]

    @property
    def croupier(self):
        return self.turn_order[-1]

    def get_cards(self, quantity_cards):
        cards = []
        for i in range(quantity_cards):
            card = self.deck.pop()
            cards.append(card)

        return cards

    def check_possible_bet(self):
        if self.game_status == "finished":
            raise GameFinishedError()

        if self.game_status == "started":
            raise GameStartedImpossibleBet()

    def change_turn(self):
        self.turn_position += 1
        player = self.turn_order[self.turn_position]
        player.set_as_playing()

    def all_players_over_the_limit(self):
        for player in self.players:
            if not player.is_over_21_points():
                return False

        self.croupier.set_as_winner()
        self.game_status = "finished"
        return True

    def check_croupier_victory(self):
        if self.all_players_over_the_limit():
            return True

        croupier_points = self.croupier.get_total_points()
        if croupier_points < 17:
            return False # The croupier can not stand with less than 17

        for player in self.players:
            if player.get_total_points() > croupier_points and not player.is_over_limit():
                return False

        self.croupier.set_as_winner()
        for player in self.players:
            if player.get_total_points() == croupier_points:
                player.set_as_winner()
                continue
            player.set_as_looser()
        self.game_status = "finished"
        return True

    def check_croupier_defeat(self):
        if self.croupier.is_over_limit():
            for player in self.players:
                if player.get_total_points() <= 21:
                    player.set_as_winner()
            self.croupier.set_as_looser()
            self.game_status = "finished"
            return True

        return False

    def get_playerId_of_current_turn(self):
        player = self.turn_order[self.turn_position]
        return str(player.player_id)

    def is_player_turn(self, player_id):
        return str(player_id) == self.get_playerId_of_current_turn()

    def deal_card_to_current_turn_player(self, player_id):

        if self.game_status == "finished":
            raise GameFinishedError()

        if not self.is_player_turn(player_id):
            raise IncorrectPlayerTurn()

        player = self.turn_order[self.turn_position]
        player.receive_cards(self.get_cards(1))

        if player.is_over_limit():
            player.set_as_looser()
            self.change_turn()

        self.all_players_over_the_limit()

    def stand_current_turn_player(self, player_id):
        if self.game_status == "finished":
            raise GameFinishedError()

        if not self.is_player_turn(player_id):
            raise IncorrectPlayerTurn()

        player = self.turn_order[self.turn_position]
        player.stand()
        self.change_turn()

    def get_player_by_id(self, player_id):
        for player in self.turn_order:
            if player.player_id == player_id:
                return player

    def place_bet_to_current_player(self, player_id, bet_amount):
        if self.game_status == "finished":
            raise GameFinishedError()
        player = self.get_player_by_id(player_id)
        player.set_bet_money(bet_amount)
        self.check_all_player_bet()

    def check_all_player_bet(self):
        players_with_bets = []
        for player in self.players:
            if player.get_bet() > 0:
                players_with_bets.append(player)
        if len(players_with_bets) == len(self.players):
            self.game_status = "started"

    def is_there_winner(self):
        if self.check_croupier_defeat():
            return True

        if self.check_croupier_victory():
            return True

        return False

    def croupier_play(self):
        if self.game_status == "finished":
            raise GameFinishedError()
        current_player_id = self.get_playerId_of_current_turn()
        if not current_player_id == str(self.croupier.player_id):
            raise NotCroupierTurnError()

        self.croupier.has_hidden_card = False
        while not self.is_there_winner():
            self.croupier.receive_cards(self.get_cards(1))

    def get_status(self):
        players_status_list = []
        for player in self.players:
            players_status_list.append(player.get_status())

        player_status_json = {
            "players_quantity": len(self.players),
            "status_game": self.game_status,
            "players": players_status_list,
            'croupier': self.croupier.get_status()
        }
        return player_status_json

    def add_players(self, players: List[Player]):
        croupier = Croupier(name="Croupier", cards=[], status="waiting_turn", has_hidden_card=True)
        self.turn_order = [croupier]
        for player in players:
            self.turn_order.insert(0, player)

    def deal_initial_cards(self):
        for player in self.turn_order:
            player.receive_cards(self.get_cards(2))
        self.turn_order[0].set_as_playing()


class NotCroupierTurnError(Exception):
    pass


class IncorrectPlayerTurn(Exception):
    pass
