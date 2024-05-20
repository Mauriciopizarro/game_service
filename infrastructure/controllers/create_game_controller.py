from typing import List
from pydantic import BaseModel
from fastapi import APIRouter, HTTPException
from application.create_game_service import CreateGameService


router = APIRouter()
create_game_service = CreateGameService()


class Player(BaseModel):
    name: str
    user_id: str

class CreateGameRequestModel(BaseModel):
    game_id: str
    players: List[Player]


@router.post("/game/create")
async def create_game(request: CreateGameRequestModel):
    create_game_service.create_game(request.players, request.game_id)