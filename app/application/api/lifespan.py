from punq import Container

from domain.events.messages import ChatCreatedRecievedFromBrokerEvent
from infrastructure.message_brokers.base import BaseMessageBroker
from project.configs import settings
from project.containers import get_container
from service_layer.mediator.base import Mediator


async def start_kafka() -> None:
    container: Container = get_container()
    message_broker: BaseMessageBroker = container.resolve(BaseMessageBroker)

    await message_broker.start()


async def consume_in_background() -> None:
    container: Container = get_container()
    message_broker: BaseMessageBroker = container.resolve(BaseMessageBroker)

    mediator: Mediator = container.resolve(Mediator)

    async for message in message_broker.start_consuming(topic=settings.KAFKA_NEW_CHATS_TOPIC):
        await mediator.publish(
            [
                ChatCreatedRecievedFromBrokerEvent(
                    chat_oid=message['chat_oid'],
                    chat_title=message['chat_title'],
                ),
            ],
        )


async def stop_kafka() -> None:
    container: Container = get_container()
    message_broker: BaseMessageBroker = container.resolve(BaseMessageBroker)

    await message_broker.close()
