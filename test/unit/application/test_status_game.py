from application.status_service import StatusService
from domain.card import LetterCard, NumberCard, As
from domain.game import Game
from domain.player import Player, Croupier
from test.utils.mock_game_repository import MockGameRepository


def get_possible_points(cards):
    total_points = 0
    total_points_list = []
    there_is_as = False

    for card in cards:
        if isinstance(card, As):
            there_is_as = True
        total_points += card.value

    total_points_list.append(total_points)
    total_points_with_as = total_points + As.special_value

    if there_is_as and total_points_with_as <= 21:
        total_points_list.append(total_points_with_as)

    if 21 in total_points_list:
        total_points_list = [21]

    return total_points_list

def get_cards(kargs):
    cards = []
    for key, value in kargs.items():
        cards.append(value)

    return cards


def get_exected_response(croupier_card_1, **kwargs):
    cards = get_cards(kwargs)
    cards_symbol = [card.symbol for card in cards]
    points = get_possible_points(cards)

    expected_response = {
        "croupier": {
            "cards": [croupier_card_1.symbol, "hidden card"],
            "is_stand": False,
            "name": "Croupier",
            "status": "waiting_turn",
            "total_points": [croupier_card_1.value]
        },
        "players": [
            {
                "cards": cards_symbol,
                "id": "63bcb88cfe7f81c8af8d9faf",
                "is_stand": False,
                "name": "Mauri",
                "status": "playing",
                "total_points": points
            }
        ],
        "players_quantity": 1,
        "status_game": "started",
    }
    return expected_response

def get_mocked_game(croupier_card_1, crupier_status="waiting_turn",has_hidden_card=True, **kwargs):

    cards = []

    for key, value in kwargs.items():
        cards.append(value)

    game = Game(
        turn_order=[
            Player(
                cards= cards,
                name="Mauri",
                player_id="63bcb88cfe7f81c8af8d9faf",
                status="playing",
                bet_amount=20
            ),
            Croupier(
                cards=[croupier_card_1, NumberCard(5)],
                name="Croupier",
                status=crupier_status,
                has_hidden_card=has_hidden_card,
            ),
        ],
        deck=[LetterCard("J"), LetterCard("Q"), NumberCard(2), As()],
        game_status= "started",
        turn_position= 0,
        game_id="63bcba244dbc3beb6fec0eb2"
    )

    return game

def test_status_game():
    # Happy path
    mocked_game = get_mocked_game(croupier_card_1=NumberCard(7), player_card_1=LetterCard("J"), player_card_2=NumberCard(5))
    expected_response = get_exected_response(croupier_card_1=NumberCard(7), player_card_1=LetterCard("J"),
                                             player_card_2=NumberCard(5))
    mock_game_repo = MockGameRepository(mocked_game)
    status_service = StatusService(game_repository=mock_game_repo)

    status_service_response = status_service.players_status(game_id="63bcba244dbc3beb6fec0eb2")

    # croupier comparations
    assert expected_response["croupier"]["name"] == status_service_response["croupier"]["name"]
    assert expected_response["croupier"]["cards"] == status_service_response["croupier"]["cards"]
    assert expected_response["croupier"]["is_stand"] == status_service_response["croupier"]["is_stand"]
    assert expected_response["croupier"]["status"] == status_service_response["croupier"]["status"]
    assert expected_response["croupier"]["total_points"] == status_service_response["croupier"]["total_points"]

    # player comparations
    assert expected_response["players"][0]["name"] == status_service_response["players"][0]["name"]
    assert expected_response["players"][0]["cards"] == status_service_response["players"][0]["cards"]
    assert expected_response["players"][0]["id"] == status_service_response["players"][0]["id"]
    assert expected_response["players"][0]["is_stand"] == status_service_response["players"][0]["is_stand"]
    assert expected_response["players"][0]["status"] == status_service_response["players"][0]["status"]
    assert expected_response["players"][0]["total_points"] == status_service_response["players"][0]["total_points"]

    # game comparations
    assert expected_response["players_quantity"] == status_service_response["players_quantity"]
    assert expected_response["status_game"] == status_service_response["status_game"]


def test_with_one_as_card_player_in_first_hand():
    mocked_game = get_mocked_game(croupier_card_1=NumberCard(7), player_card_1=As(), player_card_2=NumberCard(5))
    mock_game_repo = MockGameRepository(mocked_game)
    status_service = StatusService(game_repository=mock_game_repo)

    status_service_response = status_service.players_status(game_id="63bcba244dbc3beb6fec0eb2")

    assert status_service_response["players"][0]["total_points"] == [6,16]


def test_with_two_as_card_player_in_first_hand():
    mocked_game = get_mocked_game(croupier_card_1=NumberCard(7), player_card_1=As(), player_card_2=As())
    mock_game_repo = MockGameRepository(mocked_game)
    status_service = StatusService(game_repository=mock_game_repo)

    status_service_response = status_service.players_status(game_id="63bcba244dbc3beb6fec0eb2")

    assert status_service_response["players"][0]["total_points"] == [2,12]


def test_with_two_as_card_player_in_second_hand():
    mocked_game = get_mocked_game(croupier_card_1=NumberCard(7), player_card_1=As(), player_card_2=As(), player_card_3=NumberCard(5))
    mock_game_repo = MockGameRepository(mocked_game)
    status_service = StatusService(game_repository=mock_game_repo)

    status_service_response = status_service.players_status(game_id="63bcba244dbc3beb6fec0eb2")

    assert status_service_response["players"][0]["total_points"] == [7,17]

def test_with_two_as_discontinuous_card_player_in_second_hand():
    mocked_game = get_mocked_game(croupier_card_1=NumberCard(7), player_card_1=As(), player_card_2=LetterCard("K"), player_card_3=As())
    mock_game_repo = MockGameRepository(mocked_game)
    status_service = StatusService(game_repository=mock_game_repo)

    status_service_response = status_service.players_status(game_id="63bcba244dbc3beb6fec0eb2")

    assert status_service_response["players"][0]["total_points"] == [12]

def test_with_three_as_player():
    mocked_game = get_mocked_game(croupier_card_1=NumberCard(7), player_card_1=As(), player_card_2=As(), player_card_3=As())
    mock_game_repo = MockGameRepository(mocked_game)
    status_service = StatusService(game_repository=mock_game_repo)

    status_service_response = status_service.players_status(game_id="63bcba244dbc3beb6fec0eb2")

    assert status_service_response["players"][0]["total_points"] == [3,13]

def test_with_four_as_player():
    mocked_game = get_mocked_game(croupier_card_1=NumberCard(7), player_card_1=As(), player_card_2=As(), player_card_3=As(), player_card_4=As())
    mock_game_repo = MockGameRepository(mocked_game)
    status_service = StatusService(game_repository=mock_game_repo)

    status_service_response = status_service.players_status(game_id="63bcba244dbc3beb6fec0eb2")

    assert status_service_response["players"][0]["total_points"] == [4,14]

def test_with_four_as_and_other_card():
    mocked_game = get_mocked_game(croupier_card_1=NumberCard(7), player_card_1=As(), player_card_2=As(), player_card_3=As(), player_card_4=As(), player_card_5=NumberCard(7))
    mock_game_repo = MockGameRepository(mocked_game)
    status_service = StatusService(game_repository=mock_game_repo)

    status_service_response = status_service.players_status(game_id="63bcba244dbc3beb6fec0eb2")

    assert  status_service_response["players"][0]["total_points"] == [21]

def test_croupier_playing():
    # If croupier_status is "playing" and has_hidden_card false the second card shouldn't be hidden
    mocked_game = get_mocked_game(croupier_card_1=NumberCard(7), crupier_status="playing",has_hidden_card=False, player_card_1=As(), player_card_2=As())
    mock_game_repo = MockGameRepository(mocked_game)
    status_service = StatusService(game_repository=mock_game_repo)

    status_service_response = status_service.players_status(game_id="63bcba244dbc3beb6fec0eb2")

    assert status_service_response["croupier"]["cards"][1] == "5"