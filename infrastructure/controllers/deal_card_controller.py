from application.exceptions import IncorrectGameID, GameFinishedError, IncorrectObjectID, GamePendingBetError
from domain.game import IncorrectPlayerTurn
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from infrastructure.injector import Injector
from dependency_injector.wiring import Provide, inject


router = APIRouter()


class DealCardRequestData(BaseModel):
    user_id: str


@router.post("/game/deal_card/{game_id}")
@inject
async def deal_card_controller(game_id: str,
                               request: DealCardRequestData,
                               deal_card_service = Depends(Provide[Injector.deal_card_service])
                               ):
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
    except GamePendingBetError:
        raise HTTPException(
            status_code=400, detail='The game is pending a bet. You must make a bet first'
        )
    return {'message': "Card dealed to player"}
