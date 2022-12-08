from application.exceptions import IncorrectGameID, GameFinishedError
from application.stand_service import StandService
from domain.game import IncorrectPlayerTurn
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel

router = APIRouter()
stand_service = StandService()


class StandUserRequestData(BaseModel):
    user_id: str


@router.post("/stand/{game_id}")
async def stand_controller(game_id: str, request: StandUserRequestData):
    try:
        stand_service.stand(request.user_id, game_id)
    except IncorrectGameID:
        raise HTTPException(
            status_code=404, detail='game_id not found',
        )
    except GameFinishedError:
        raise HTTPException(
            status_code=400, detail='The game_id entered is finished',
        )
    except IncorrectPlayerTurn:
        raise HTTPException(
            status_code=400, detail='Is not a turn to player entered',
        )
    return {'message': "Player stand"}
