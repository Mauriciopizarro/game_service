from fastapi import FastAPI
import infrastructure.injector # no remove this dependecy
from infrastructure.controllers import stand_controller, deal_card_controller, status_controller, croupier_controller, \
    history_game_controller

app = FastAPI()

app.include_router(history_game_controller.router)
app.include_router(status_controller.router)
app.include_router(deal_card_controller.router)
app.include_router(stand_controller.router)
app.include_router(croupier_controller.router)
