from application.deal_card_service import DealCardService
from domain.card import LetterCard, NumberCard
from domain.game import Game, IncorrectPlayerTurn
from domain.player import Player, Croupier
from test.utils.mock_game_repository import MockGameRepository
import pytest

def create_mock_game(last_card_to_deal):
    return Game(
        turn_order=[
            Player(
                cards=[LetterCard("J"), NumberCard(8)],
                name= "Mauri",
                player_id= "63bcb88cfe7f81c8af8d9faf",
                status= "playing",
                bet_amount=20
            ),
            Croupier(
                cards=[LetterCard("J"), NumberCard(8)],
                name="Croupier",
                status="waiting_turn",
                has_hidden_card= True,
            ),
        ],
        deck=[LetterCard("J"), LetterCard("Q"), NumberCard(2), NumberCard(last_card_to_deal)],
        game_status= "started",
        turn_position= 0,
        game_id= "63bcba244dbc3beb6fec0eb2"
    )
def test_deal_card():
    game = create_mock_game(2) # With a 2 the player does not win
    mock_game_repo = MockGameRepository(game)
    deal_card_service = DealCardService(game_repository=mock_game_repo)

    deal_card_service.deal_card(player_id="63bcb88cfe7f81c8af8d9faf", game_id="63bcba244dbc3beb6fec0eb2")

    assert len(game.turn_order[0].cards) == 3
    assert game.turn_order[0].cards[-1] == NumberCard(2)
    assert game.turn_order[0].status == "playing"
    assert game.turn_order[1].status == "waiting_turn"
    assert game.game_status == "started"

 

 
def test_deal_card_when_player_win():
    game = create_mock_game(3) # With a 3 the player wins
    mock_game_repo = MockGameRepository(game)
    deal_card_service = DealCardService(game_repository=mock_game_repo)

    deal_card_service.deal_card(player_id="63bcb88cfe7f81c8af8d9faf", game_id="63bcba244dbc3beb6fec0eb2")

    assert len(game.turn_order[0].cards) == 3
    assert game.turn_order[0].cards[-1] == NumberCard(3)
    assert game.turn_order[0].status == "playing"
    assert game.turn_order[1].status == "waiting_turn"
    assert game.game_status == "started"


def test_deal_card_when_player_loose():
    game = create_mock_game(4) # With a 4 the player loose
    mock_game_repo = MockGameRepository(game)
    deal_card_service = DealCardService(game_repository=mock_game_repo)

    deal_card_service.deal_card(player_id="63bcb88cfe7f81c8af8d9faf", game_id="63bcba244dbc3beb6fec0eb2")

    assert len(game.turn_order[0].cards) == 3
    assert game.turn_order[0].cards[-1] == NumberCard(4)
    assert game.turn_order[0].status == "looser"
    assert game.turn_order[1].status == "winner"
    assert game.game_status == "finished"

def test_deal_card_when_player_id_is_incorrect():
    game = create_mock_game(4)
    mock_game_repo = MockGameRepository(game)
    deal_card_service = DealCardService(game_repository=mock_game_repo)

    with pytest.raises(IncorrectPlayerTurn):
        deal_card_service.deal_card(player_id="63bcb88cfe7f81c8af8d9fag", game_id="63bcba244dbc3beb6fec0eb2") #player_id incorrect
