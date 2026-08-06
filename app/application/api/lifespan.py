from punq import Container

from infrastructure.message_brokers.base import BaseMessageBroker
from project.containers import get_container


async def start_kafka() -> None:
    container: Container = get_container()
    message_broker: BaseMessageBroker = container.resolve(BaseMessageBroker)

    await message_broker.start()


async def stop_kafka() -> None:
    container: Container = get_container()
    message_broker: BaseMessageBroker = container.resolve(BaseMessageBroker)

    await message_broker.close()
