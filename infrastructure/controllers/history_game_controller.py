from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
from application.exceptions import EmptyHistory
from application.history_game_service import HistoryGamesService


router = APIRouter()
history_games_service = HistoryGamesService()


class HistoryGamesModelResponse(BaseModel):
    game_id: str
    status: str
    player_status: str


class ResponseModelHistoryGames(BaseModel):
    quantity: int
    results: List[HistoryGamesModelResponse]


@router.get("/player/history/{user_id}", response_model=ResponseModelHistoryGames)
async def history_game_controller(user_id: str):
    try:
        history_dict = history_games_service.get_history(user_id=user_id)
        return ResponseModelHistoryGames(quantity=len(history_dict), results=history_dict)
    except EmptyHistory:
        raise HTTPException(
            status_code=404, detail='History not found or inexistent user_id',
        )
