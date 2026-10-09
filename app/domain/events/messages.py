from dataclasses import dataclass
from typing import ClassVar

from domain.events.base import BaseEvent


@dataclass
class NewMessageReceivedEvent(BaseEvent):
    event_title: ClassVar[str] = 'New Message Received'

    chat_oid: str
    message_text: str
    message_oid: str


@dataclass
class NewChatCreatedEvent(BaseEvent):
    event_title: ClassVar[str] = 'New Chat Created'

    chat_oid: str
    chat_title: str


@dataclass
class ChatCreatedRecievedFromBrokerEvent(BaseEvent):
    event_title: ClassVar[str] = 'Chat Created Recieved From Broker'

    chat_oid: str
    chat_title: str
