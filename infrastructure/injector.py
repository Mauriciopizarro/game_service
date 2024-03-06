from infrastructure.repositories.game_mongo_repository import GameMongoRepository
from infrastructure.repositories.game_mysql_repository import GameSqlRepository
from infrastructure.event_managers.rabbit_publisher import RabbitPublisher
from dependency_injector import containers, providers


class Injector(containers.DeclarativeContainer):

    game_repo = providers.Singleton(GameMongoRepository)
    publisher = providers.Singleton(RabbitPublisher)


injector = Injector()
injector.wire(modules=["application.create_game_service",
                       "application.croupier_service",
                       "application.deal_card_service",
                       "application.stand_service",
                       "application.status_service",
                       "application.history_game_service",
                       "application.make_bet_service"
                       ])
