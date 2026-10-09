import logging
from dataclasses import (
    asdict,
    dataclass,
)

from domain.events.messages import (
    ChatCreatedRecievedFromBrokerEvent,
    NewChatCreatedEvent,
)
from infrastructure.message_brokers.converters import convert_event_to_message_broker
from service_layer.events.base import EventHandler


logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class NewChatCreatedEventHanlder(EventHandler[NewChatCreatedEvent, None]):
    async def handle(self, event: NewChatCreatedEvent) -> None:
        await self.message_broker.send_message(
            key=str(event.event_id).encode(),
            topic=self.broker_topic,
            value=convert_event_to_message_broker(event=event),
        )
        logger.debug('Обработалось событие: %s', event.event_title)


@dataclass(frozen=True)
class ChatCreatedRecievedFromBrokerEventHandler(EventHandler[ChatCreatedRecievedFromBrokerEvent, None]):
    async def handle(self, event: ChatCreatedRecievedFromBrokerEvent) -> None:
        logger.info('event recieved from broker: %s', asdict(event))
