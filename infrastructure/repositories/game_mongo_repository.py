import json
from pymongo import MongoClient
from bson.objectid import ObjectId
from bson.json_util import dumps
from application.exceptions import IncorrectGameID, IncorrectObjectID, EmptyHistory
from domain.card import NumberCard, As, LetterCard
from domain.game import Game
from domain.interfaces.game_repository import GameRepository
from domain.player import Player, Croupier


class GameMongoRepository(GameRepository):

    instance = None

    def __init__(self):
        self.db = self.get_database()

    # Patron singleton
    @classmethod
    def get_instance(cls):
        if not cls.instance:
            cls.instance = cls()

        return cls.instance

    @staticmethod
    def get_database():
        client = MongoClient("mongodb://mongo:27017/blackjack")
        return client['blackjack']["games"]

    def get_by_user_id(self, user_id: str) -> dict:
        pymongo_cursor = self.db.find({"turn_order.player_id": user_id})
        quantity_results = pymongo_cursor.explain().get("executionStats").get("nReturned")
        if not quantity_results > 0:
            raise EmptyHistory()
        json_data = dumps(pymongo_cursor)
        json_response = json.loads(json_data)
        formated_response = self.format_model_response(user_id, json_response)
        return formated_response

    def get(self, game_id: str) -> Game:
        if not ObjectId.is_valid(game_id):
            raise IncorrectObjectID()
        game_dict = self.db.find_one({"_id": ObjectId(game_id)})
        if not game_dict:
            raise IncorrectGameID()
        game_status = game_dict["game_status"]
        deck = []
        turn_order = []
        turn_position = game_dict["turn_position"]
        croupier = game_dict["turn_order"].pop()
        for card in game_dict["deck"]:
            deck.append(self.get_card_object(card))
        for player in game_dict["turn_order"]:
            turn_order.append(self.get_player_object(player, False))
        turn_order.append(self.get_player_object(croupier, True))
        game = Game(turn_order=turn_order, deck=deck, game_status=game_status, turn_position=turn_position, game_id=game_id)
        return game

    def save(self, game: Game) -> Game:
        game_dict = game.dict()
        game_dict["_id"] = ObjectId(game.game_id)
        game_dict.pop("game_id")
        self.db.insert_one(game_dict)
        return Game(turn_order=game.turn_order, deck=game.deck, game_status=game.game_status, turn_position=game.turn_position, game_id=game.game_id)

    def update(self, game: Game) -> Game:
        game_dict = game.dict()
        game_dict.pop("game_id")
        self.db.find_one_and_update({"_id": ObjectId(game.game_id)}, {"$set": game_dict})
        return Game(turn_order=game.turn_order, deck=game.deck, game_status=game.game_status, turn_position=game.turn_position, game_id=game.game_id)

    def get_player_object(self, player_dict, is_croupier):
        if not is_croupier:
            player_cards = []
            for card in player_dict["cards"]:
                player_cards.append(self.get_card_object(card))
            return Player(name=player_dict["name"], player_id=player_dict["player_id"], cards=player_cards, status=player_dict["status"])

        player_cards = []
        for card in player_dict["cards"]:
            player_cards.append(self.get_card_object(card))
        return Croupier(name=player_dict["name"], cards=player_cards, status=player_dict["status"], has_hidden_card=player_dict["has_hidden_card"])

    @staticmethod
    def get_card_object(card_dict):
        if card_dict["type"] == "NumberCard":
            return NumberCard(card_dict["value"])
        elif card_dict["type"] == "LetterCard":
            return LetterCard(card_dict["symbol"])
        elif card_dict["type"] == "As":
            return As()

    @staticmethod
    def format_model_response(user_id: str, json_response: dict) -> dict:
        """
                # Model returned by method
                "model_response":{
                    "game_id": game_id,
                    "status": game_status,
                    "player_status": status_player
                }
        """
        # Remove and reformat the keys like model response
        for results in json_response:
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

        return json_response
