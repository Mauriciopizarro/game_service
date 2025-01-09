from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List
from application.exceptions import EmptyHistory
from infrastructure.injector import Injector
from dependency_injector.wiring import Provide, inject


router = APIRouter()


class HistoryGamesModelResponse(BaseModel):
    game_id: str
    status: str
    player_status: str


class ResponseModelHistoryGames(BaseModel):
    quantity: int
    results: List[HistoryGamesModelResponse]


@router.get("/player/history/{user_id}", response_model=ResponseModelHistoryGames)
@inject
async def history_game_controller(user_id: str,
                                  history_games_service = Depends(Provide[Injector.history_of_games_service])
                                  ):
    try:
        history_dict = history_games_service.get_history(user_id=user_id)
        return ResponseModelHistoryGames(quantity=len(history_dict), results=history_dict)
    except EmptyHistory:
        raise HTTPException(
            status_code=404, detail='Empty history or nonexistent user_id',
        )
