from application.stand_service import StandService
from domain.card import LetterCard, NumberCard
from domain.game import Game
from domain.player import Player, Croupier
from test.utils.mock_game_repository import MockGameRepository


def test_stand_player():
    game = Game(
        turn_order=[
            Player(
                cards=[LetterCard("J"), NumberCard(8)],
                name="Mauri",
                player_id="63bcb88cfe7f81c8af8d9faf",
                status="playing",
            ),
            Croupier(
                cards=[LetterCard("J"), NumberCard(8)],
                name="Croupier",
                status="waiting_turn",
                has_hidden_card=True,
            ),
        ],
        deck=[LetterCard("J"), LetterCard("Q"), NumberCard(2)],
        game_status="started",
        turn_position=0,
        game_id="63bcba244dbc3beb6fec0eb2"
    )
    mock_game_repo = MockGameRepository(game)
    stand_service = StandService(game_repository=mock_game_repo)
    stand_service.stand(player_id="63bcb88cfe7f81c8af8d9faf", game_id="63bcba244dbc3beb6fec0eb2")

    assert game.turn_order[0].status == "waiting_croupier"
    assert game.turn_position == 1
    assert game.turn_order[1].status == "playing"
