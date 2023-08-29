# from application.exceptions import IncorrectGameID, IncorrectObjectID, GameFinishedError
# from application.deal_card_service import DealCardService
# from domain.game import IncorrectPlayerTurn
# from fastapi.testclient import TestClient
# from unittest.mock import patch
# from main import app
#
# client = TestClient(app)
#
# @patch.object(DealCardService, 'deal_card')
# def test_deal_card(mock_deal_card):
#     response = client.post("/game/deal_card/1", json={"user_id": "2"})
#
#     assert response.status_code == 200
#     assert response.json() == {'message': "Card dealed to player"}
#     mock_deal_card.assert_called_once_with("2", "1")
#
# @patch.object(DealCardService, 'deal_card', side_effect=IncorrectGameID())
# def test_deal_card_with_incorrect_game_id(mock_deal_card):
#     response = client.post("/game/deal_card/1", json={"user_id": "2"})
#     assert response.status_code == 404
#     assert response.json() == {'detail': "game_id not found"}
#
# @patch.object(DealCardService, 'deal_card', side_effect=IncorrectObjectID())
# def test_deal_card_with_incorrect_object_id(mock_deal_card):
#     response = client.post("/game/deal_card/1", json={"user_id": "2"})
#     assert response.status_code == 400
#     assert response.json() == {'detail': "incorrect game_id"}
#
# @patch.object(DealCardService, 'deal_card', side_effect=GameFinishedError())
# def test_deal_card_with_game_finished(mock_deal_card):
#     response = client.post("/game/deal_card/1", json={"user_id": "2"})
#     assert response.status_code == 400
#     assert response.json() == {'detail': "The game_id entered is finished"}
#
# @patch.object(DealCardService, 'deal_card', side_effect=IncorrectPlayerTurn())
# def test_deal_card_with_incorrect_player_turn(mock_deal_card):
#     response = client.post("/game/deal_card/1", json={"user_id": "2"})
#     assert response.status_code == 400
#     assert response.json() == {'detail': "Is not a turn to player entered or id may be incorrect"}