from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Optional
from infrastructure.injector import Injector
from dependency_injector.wiring import Provide, inject
from application.exceptions import IncorrectGameID, IncorrectObjectID

router = APIRouter()


class Player(BaseModel):
    cards: List[str]
    id: str
    is_stand: bool
    name: str
    status: str
    total_points: List[int]
    bet_amount: int


class Croupier(BaseModel):
    cards: List[str]
    is_stand: bool
    name: str
    status: str
    total_points: List[int]


class StatusResponse(BaseModel):
    croupier: Croupier
    players: List[Player]
    players_quantity: int
    status_game: str


@router.get("/game/status/{game_id}", response_model=StatusResponse)
@inject
async def get_status_controller(game_id: str,
                                status_service = Depends(Provide[Injector.status_servie])
                                ):
    try:
        player_status_json = status_service.players_status(game_id)
        return player_status_json
    except IncorrectGameID:
        raise HTTPException(
            status_code=404, detail='game not found',
        )
    except IncorrectObjectID:
        raise HTTPException(
            status_code=400, detail='incorrect format of game_id',
        )
