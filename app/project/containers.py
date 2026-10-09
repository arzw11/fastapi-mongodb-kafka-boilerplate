from functools import lru_cache

from aiokafka import (
    AIOKafkaConsumer,
    AIOKafkaProducer,
)
from motor.motor_asyncio import AsyncIOMotorClient
from punq import (
    Container,
    Scope,
)

from domain.events.messages import (
    ChatCreatedRecievedFromBrokerEvent,
    NewChatCreatedEvent,
)
from infrastructure.message_brokers.base import BaseMessageBroker
from infrastructure.message_brokers.kafka import KafkaMessageBroker
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
from service_layer.events.messages import (
    ChatCreatedRecievedFromBrokerEventHandler,
    NewChatCreatedEventHanlder,
)
from service_layer.mediator.base import Mediator
from service_layer.queries.messages import (
    GetChatDetailQuery,
    GetChatDetailQueryHandler,
    GetMessagesQuery,
    GetMessagesQueryHandler,
)


@lru_cache(1)
def get_container() -> Container:
    return _init_container()


def _init_container() -> Container:
    container: Container = Container()

    # database
    def create_mongodb_client():
        return AsyncIOMotorClient(
            settings.MONGO_DB_CONNECTION_URI,
            serverSelectionTimeoutMS=3000,
        )

    container.register(AsyncIOMotorClient, factory=create_mongodb_client, scope=Scope.singleton)
    mongodb_client = container.resolve(AsyncIOMotorClient)

    # repositories
    def init_chat_mongo_db_repository() -> BaseChatsRepository:
        return MongoDBChatsRepository(
            mongo_db_client=mongodb_client,
            mongo_db_db_title=settings.MONGODB_CHAT_DATABASE,
            mongo_db_collection_title=settings.MONGODB_CHAT_COLLECTION,
        )

    def init_messages_mongodb_repository() -> BaseMessagesRepository:
        return MongoDBMessagesRepository(
            mongo_db_client=mongodb_client,
            mongo_db_db_title=settings.MONGODB_CHAT_DATABASE,
            mongo_db_collection_title=settings.MONGODB_MESSAGES_COLLECTION,
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

    # message broker
    def init_kafka_message_broker() -> BaseMessageBroker:
        return KafkaMessageBroker(
            producer=AIOKafkaProducer(bootstrap_servers=settings.kafka_url),
            consumer=AIOKafkaConsumer(
                bootstrap_servers=settings.kafka_url,
                metadata_max_age_ms=300000,
            ),
        )

    container.register(
        service=BaseMessageBroker,
        factory=init_kafka_message_broker,
        scope=Scope.singleton,
    )

    def init_mediator() -> Mediator:
        mediator: Mediator = Mediator()

        # events
        mediator.register_event(
            NewChatCreatedEvent,
            [
                NewChatCreatedEventHanlder(
                    message_broker=container.resolve(BaseMessageBroker),
                    broker_topic=settings.KAFKA_NEW_CHATS_TOPIC,
                ),
            ],
        )
        mediator.register_event(
            ChatCreatedRecievedFromBrokerEvent,
            [
                ChatCreatedRecievedFromBrokerEventHandler(
                    message_broker=container.resolve(BaseMessageBroker),
                    broker_topic=settings.KAFKA_NEW_CHATS_TOPIC,
                ),
            ],
        )

        # commands
        mediator.register_command(
            CreateChatCommand,
            [
                CreateChatCommandHandler(
                    _mediator=mediator,
                    chat_repository=container.resolve(BaseChatsRepository),
                ),
            ],
        )
        mediator.register_command(
            CreateMessageCommand,
            [
                CreateMessageCommandHandler(
                    _mediator=mediator,
                    chat_repository=container.resolve(BaseChatsRepository),
                    message_repository=container.resolve(BaseMessagesRepository),
                ),
            ],
        )

        # queries
        mediator.register_query(
            GetChatDetailQuery,
            GetChatDetailQueryHandler(chat_repository=container.resolve(BaseChatsRepository)),
        )
        mediator.register_query(
            GetMessagesQuery,
            GetMessagesQueryHandler(messages_repository=container.resolve(BaseMessagesRepository)),
        )

        return mediator

    container.register(Mediator, init_mediator)

    return container
