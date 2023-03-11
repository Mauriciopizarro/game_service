import pytest
from application.create_game_service import CreateGameService
from application.exceptions import EmptyPlayersList, IncorrectGameID
from test.utils.mock_game_repository import MockGameRepository

mock_game_repo = MockGameRepository()
create_service = CreateGameService(game_repository=mock_game_repo)
players = [
    {
        "name": "test",
        "user_id": "1"
    },
    {
        "name": "Mauri",
        "user_id": "2"
    }
]

def test_create_game():
    # Happy path
    game_saved = create_service.create_game(players=players, game_id="63bcba244dbc3beb6fec0eb2")

    assert game_saved.turn_order[0].status == "playing"
    assert game_saved.turn_order[0].player_id == "2"
    assert game_saved.turn_order[0].name == "Mauri"
    assert game_saved.turn_position == 0
    assert len(game_saved.turn_order[0].cards) == 2
    assert len(game_saved.turn_order[-1].cards) == 2
    assert game_saved.turn_order[-1].name == "Croupier"
    assert game_saved.turn_order[-1].has_hidden_card == True
    assert game_saved.turn_order[-1].status == "waiting_turn"

def test_empty_players_list():
    # If players is empty raise exception EmptyPlayersList
    with pytest.raises(EmptyPlayersList) as e:
        create_service.create_game(players=[],game_id="63bcba244dbc3beb6fec0eb2") # Players list empty
        assert str(e.value) == 'Empty players_list, please check if the event has sent correctly the message'

def test_empty_game_id():
    # If game_id is empty raise exception EmptyPlayersList
    with pytest.raises(IncorrectGameID) as e:
        create_service.create_game(players=players,game_id="") # Game_id empty
        assert str(e.value) == 'Empty game_id, please check if the event has sent correctly the message'
