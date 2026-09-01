from fastapi import FastAPI
from infrastructure.injector import Injector
from infrastructure.controllers import stand_controller, deal_card_controller, status_controller, \
    history_game_controller, create_game_controller, make_bet_controller


app = FastAPI()
injector = Injector()
app.container = injector

app.include_router(history_game_controller.router)
app.include_router(status_controller.router)
app.include_router(deal_card_controller.router)
app.include_router(stand_controller.router)
app.include_router(create_game_controller.router)
app.include_router(make_bet_controller.router)
