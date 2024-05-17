from dependency_injector.wiring import Provide, inject
from fastapi import HTTPException
from config import settings
from application.exceptions import InvalidBetAmountException
from domain.interfaces.game_repository import GameRepository
from infrastructure.injector import Injector
import requests
from requests.exceptions import HTTPError


class MakeBetService:

    @inject
    def __init__(self, game_repository: GameRepository = Provide[Injector.game_repo]):
        self.game_repository = game_repository

    def place_bet(self, game_id, player_id, bet_amount):
        try:
            if bet_amount < 1:
                raise InvalidBetAmountException()
            game = self.game_repository.get(game_id)
            # if is the player turn and game is not finished is possible put the bet
            game.check_possible_bet()
            url = f'{settings.WALLET_API_URL}/wallet/money_out'
            response = requests.post(url, json={
                'user_id': player_id,
                'amount': bet_amount
            })
            response.raise_for_status()
        except HTTPError as e:
            raise HTTPException(
                status_code=response.status_code, detail=response.json().get('detail'),
            )
        if response.status_code == 200:
            game.place_bet_to_current_player(player_id, bet_amount)
            self.game_repository.update(game)
