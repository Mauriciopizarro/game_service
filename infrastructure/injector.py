from application.create_game_service import CreateGameService
from application.deal_card_service import DealCardService
from application.history_game_service import HistoryGamesService
from application.make_bet_service import MakeBetService
from application.stand_service import StandService
from application.status_service import StatusService
from infrastructure.repositories.game_mongo_repository import GameMongoRepository
from infrastructure.event_managers.rabbit_publisher import RabbitPublisher
from dependency_injector import containers, providers


class Injector(containers.DeclarativeContainer):

    game_repo = providers.Singleton(GameMongoRepository)
    publisher = providers.Singleton(RabbitPublisher)
    create_game_service = providers.Singleton(CreateGameService)
    deal_card_service = providers.Singleton(DealCardService)
    history_of_games_service = providers.Singleton(HistoryGamesService)
    bet_service = providers.Singleton(MakeBetService)
    stand_service = providers.Singleton(StandService)
    status_servie = providers.Singleton(StatusService)

    wiring_config = containers.WiringConfiguration(modules=[
        "infrastructure.controllers.create_game_controller",
        "infrastructure.controllers.deal_card_controller",
        "infrastructure.controllers.history_game_controller",
        "infrastructure.controllers.make_bet_controller",
        "infrastructure.controllers.stand_controller",
        "infrastructure.controllers.status_controller",
    ])

