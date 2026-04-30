from functools import lru_cache

from motor.motor_asyncio import AsyncIOMotorClient
from punq import (
    Container,
    Scope,
)

from infrastructure.repositories.messages.base import BaseChatRepository
from infrastructure.repositories.messages.mongo import MongoDBChatRepository
from project.configs import settings
from service_layer.commands.messages import (
    CreateChatCommand,
    CreateChatCommandHandler,
)
from service_layer.mediator import Mediator


@lru_cache(1)
def get_container() -> Container:
    return _init_container()


def _init_container() -> Container:
    container: Container = Container()

    container.register(CreateChatCommandHandler)

    def init_chat_mongo_db_repository() -> MongoDBChatRepository:
        return MongoDBChatRepository(
            mongo_db_client=AsyncIOMotorClient(
                settings.MONGO_DB_CONNECTION_URI,
                serverSelectionTimeoutMS=3000,
            ),
            mongo_db_db_title=settings.MONGODB_CHAT_DATABASE,
            mongo_db_collection_title=settings.MONGODB_CHAT_COLLECTION,
        )

    def init_mediator() -> Mediator:
        mediator: Mediator = Mediator()

        mediator.register_command(
            CreateChatCommand,
            [CreateChatCommandHandler(chat_repository=container.resolve(BaseChatRepository))],
        )

        return mediator

    container.register(
        service=BaseChatRepository,
        factory=init_chat_mongo_db_repository,
        scope=Scope.singleton,
    )
    container.register(Mediator, init_mediator)

    return container
