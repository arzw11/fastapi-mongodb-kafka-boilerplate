from datetime import datetime

from pydantic import BaseModel

from domain.entities.messages import (
    Chat,
    Message,
)


class CreateChatInSchema(BaseModel):
    title: str


class CreateChatOutSchema(BaseModel):
    oid: str
    title: str

    @classmethod
    def from_entity(cls, chat: Chat) -> 'CreateChatOutSchema':
        return cls(
            oid=chat.oid,
            title=chat.title.as_generic_type(),
        )


class CreateMessageSchema(BaseModel):
    text: str


class CreateMessageResponseSchema(BaseModel):
    text: str
    oid: str

    @classmethod
    def from_entity(cls, message: Message) -> 'CreateMessageResponseSchema':
        return cls(text=message.text.as_generic_type(), oid=message.oid)


class ChatDetailSchema(BaseModel):
    oid: str
    title: str
    created_at: datetime

    @classmethod
    def from_entity(cls, chat: Chat) -> 'ChatDetailSchema':
        return cls(
            oid=chat.oid,
            title=chat.title.as_generic_type(),
            created_at=chat.created_at,
        )
