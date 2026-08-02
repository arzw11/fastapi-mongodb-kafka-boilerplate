from functools import lru_cache

from motor.motor_asyncio import AsyncIOMotorClient
from punq import (
    Container,
    Scope,
)

from infrastructure.repositories.messages.base import (
    BaseChatsRepository,
    BaseMessagesRepository,
)
from infrastructure.repositories.messages.mongo import (
    MongoDBChatsRepository,
    MongoDBMessagesRepository,
)
from project.configs import settings
from service_layer.commands.messages import (
    CreateChatCommand,
    CreateChatCommandHandler,
    CreateMessageCommand,
    CreateMessageCommandHandler,
)
from service_layer.mediator import Mediator
from service_layer.queries.messages import (
    GetChatDetailQuery,
    GetChatDetailQueryHandler,
)


@lru_cache(1)
def get_container() -> Container:
    return _init_container()


def _init_container() -> Container:
    container: Container = Container()

    container.register(CreateChatCommandHandler)

    def create_mongodb_client():
        return AsyncIOMotorClient(
            settings.MONGO_DB_CONNECTION_URI,
            serverSelectionTimeoutMS=3000,
        )

    container.register(AsyncIOMotorClient, factory=create_mongodb_client, scope=Scope.singleton)
    mongodb_client = container.resolve(AsyncIOMotorClient)

    def init_chat_mongo_db_repository() -> MongoDBChatsRepository:
        return MongoDBChatsRepository(
            mongo_db_client=mongodb_client,
            mongo_db_db_title=settings.MONGODB_CHAT_DATABASE,
            mongo_db_collection_title=settings.MONGODB_CHAT_COLLECTION,
        )

    def init_messages_mongodb_repository() -> BaseMessagesRepository:
        return MongoDBMessagesRepository(
            mongo_db_client=mongodb_client,
            mongo_db_db_title=settings.MONGODB_CHAT_DATABASE,
            mongo_db_collection_title=settings.MONGODB_CHAT_COLLECTION,
        )

    container.register(
        service=BaseChatsRepository,
        factory=init_chat_mongo_db_repository,
        scope=Scope.singleton,
    )
    container.register(
        service=BaseMessagesRepository,
        factory=init_messages_mongodb_repository,
        scope=Scope.singleton,
    )

    def init_mediator() -> Mediator:
        mediator: Mediator = Mediator()

        mediator.register_command(
            CreateChatCommand,
            [CreateChatCommandHandler(chat_repository=container.resolve(BaseChatsRepository))],
        )
        mediator.register_command(
            CreateMessageCommand,
            [
                CreateMessageCommandHandler(
                    chat_repository=container.resolve(BaseChatsRepository),
                    message_repository=container.resolve(BaseMessagesRepository),
                ),
            ],
        )

        mediator.register_query(
            GetChatDetailQuery,
            [GetChatDetailQueryHandler(chat_repository=container.resolve(BaseChatsRepository))],
        )

        return mediator

    container.register(Mediator, init_mediator)

    return container
