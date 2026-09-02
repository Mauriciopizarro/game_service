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


class BatchStatusRequest(BaseModel):
    game_ids: List[str]


class BatchGameStatus(BaseModel):
    game_id: str
    status_game: str


class BatchStatusResponse(BaseModel):
    games: List[BatchGameStatus]


@router.post("/game/status/batch", response_model=BatchStatusResponse)
@inject
async def get_status_batch_controller(request: BatchStatusRequest,
                                      status_service = Depends(Provide[Injector.status_servie])):
    """Devuelve el estado de N partidas en 1 sola llamada.

    Reemplaza el N+1 que hacía el gateway pidiendo /game/status/{game_id}
    por cada partida del lobby. Los ids que no existen o son inválidos se
    omiten del resultado.
    """
    statuses = status_service.statuses_by_ids(request.game_ids)
    games = [
        BatchGameStatus(game_id=gid, status_game=status)
        for gid, status in statuses.items()
    ]
    return BatchStatusResponse(games=games)
