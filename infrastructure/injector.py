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
    create_game_service = providers.Factory(
        CreateGameService,
        game_repository=game_repo)
    deal_card_service = providers.Factory(
        DealCardService,
        game_repository=game_repo,
        publisher=publisher)
    history_of_games_service = providers.Factory(
        HistoryGamesService,
        game_repository=game_repo)
    bet_service = providers.Factory(
        MakeBetService,
        game_repository=game_repo)
    stand_service = providers.Factory(
        StandService,
        game_repository=game_repo,
        publisher=publisher)
    status_servie = providers.Factory(
        StatusService,
        game_repository=game_repo)

    wiring_config = containers.WiringConfiguration(modules=[
        "infrastructure.controllers.create_game_controller",
        "infrastructure.controllers.deal_card_controller",
        "infrastructure.controllers.history_game_controller",
        "infrastructure.controllers.make_bet_controller",
        "infrastructure.controllers.stand_controller",
        "infrastructure.controllers.status_controller",
    ])

