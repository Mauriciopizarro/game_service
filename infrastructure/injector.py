from infrastructure.repositories.game_mongo_repository import GameMongoRepository
from dependency_injector import containers, providers


class Injector(containers.DeclarativeContainer):

    game_repo = providers.Singleton(GameMongoRepository)


injector = Injector()
injector.wire(modules=["application.create_game_service",
                       "application.croupier_service",
                       "application.deal_card_service",
                       "application.stand_service",
                       "application.status_service"
                       ])
