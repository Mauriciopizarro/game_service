from typing import List
from pydantic import BaseModel
from fastapi import APIRouter, HTTPException, Depends
from infrastructure.injector import Injector
from dependency_injector.wiring import Provide, inject


router = APIRouter()


class Player(BaseModel):
    name: str
    user_id: str

class CreateGameRequestModel(BaseModel):
    game_id: str
    players: List[Player]


@router.post("/game/create")
@inject
async def create_game(request: CreateGameRequestModel,
                      create_game_service = Depends(Provide[Injector.create_game_service])
                      ):
    create_game_service.create_game(request.players, request.game_id)