from application.deal_card_service import DealCardService
from application.exceptions import IncorrectGameID, GameFinishedError, IncorrectObjectID
from domain.game import IncorrectPlayerTurn
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel

deal_card_service = DealCardService()
router = APIRouter()


class DealCardRequestData(BaseModel):
    user_id: str


@router.post("/deal_card/{game_id}")
async def deal_card_controller(game_id: str, request: DealCardRequestData):
    try:
        deal_card_service.deal_card(request.user_id, game_id)
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
            status_code=400, detail='The game_id entered is finished'
        )
    except IncorrectPlayerTurn:
        raise HTTPException(
            status_code=400, detail='Is not a turn to player entered or id may be incorrect'
        )
    return {'message': "Card dealed to player"}
