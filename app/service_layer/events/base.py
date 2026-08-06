from abc import (
    ABC,
    abstractmethod,
)
from dataclasses import (
    dataclass,
    field,
)
from typing import (
    Any,
    Generic,
    TypeVar,
)

from domain.events.base import BaseEvent
from infrastructure.message_brokers.base import BaseMessageBroker


ET = TypeVar('ET', bound=BaseEvent)
ER = TypeVar('ER', bound=Any)


@dataclass(frozen=True)
class EventHandler(ABC, Generic[ET, ER]):
    message_broker: BaseMessageBroker
    broker_topic: str | None = field(default=None, kw_only=True)

    @abstractmethod
    async def handle(self, event: ET) -> ER:
        ...
