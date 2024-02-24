from pydantic import BaseModel
from domain.game import IncorrectPlayerTurn
from fastapi import APIRouter, HTTPException, Depends
from application.make_bet_service import MakeBetService
from application.exceptions import IncorrectGameID, GameFinishedError, IncorrectObjectID

router = APIRouter()
bet_service = MakeBetService()


class PlaceBetRequestData(BaseModel):
    player_id: str
    bet_amount: int


@router.post("/game/make_bet/{game_id}")
async def make_bet_controller(game_id: str, request: PlaceBetRequestData):
    try:
        bet_service.place_bet(game_id, request.player_id, request.bet_amount)
    except IncorrectGameID:
        raise HTTPException(
            status_code=404, detail='game_id not found',
        )
    except IncorrectObjectID:
        raise HTTPException(
            status_code=400, detail='incorrect game_id',
        )
    except GameFinishedError:
        raise HTTPException(
            status_code=400, detail='The game_id entered is finished',
        )
    except IncorrectPlayerTurn:
        raise HTTPException(
            status_code=400, detail='Is not a turn to player entered',
        )
    return {'message': "Your bet is successfully set"}
