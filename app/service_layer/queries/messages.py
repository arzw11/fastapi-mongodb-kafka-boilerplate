from dataclasses import dataclass
from mailbox import Message
from typing import Iterable

from domain.entities.messages import Chat
from infrastructure.repositories.filters.messages import GetMessagesFilters
from infrastructure.repositories.messages.base import (
    BaseChatsRepository,
    BaseMessagesRepository,
)
from service_layer.exceptions.messages import ChatNotFoundException
from service_layer.queries.base import (
    BaseQuery,
    QueryHandler,
)


@dataclass(frozen=True)
class GetChatDetailQuery(BaseQuery):
    chat_oid: str


@dataclass(frozen=True)
class GetChatDetailQueryHandler(QueryHandler[GetChatDetailQuery, Chat]):
    chat_repository: BaseChatsRepository

    async def handle(self, query: GetChatDetailQuery) -> Chat:
        chat = await self.chat_repository.get_chat_by_oid(query.chat_oid)

        if not chat:
            raise ChatNotFoundException(chat_oid=query.chat_oid)

        return chat


@dataclass(frozen=True)
class GetMessagesQuery(BaseQuery):
    chat_oid: str
    filters: GetMessagesFilters


@dataclass(frozen=True)
class GetMessagesQueryHandler(QueryHandler[GetMessagesQuery, Iterable[Message]]):
    messages_repository: BaseMessagesRepository

    async def handle(self, query: GetMessagesQuery) -> Iterable[Message]:
        return await self.messages_repository.get_messages(
            chat_oid=query.chat_oid,
            filters=query.filters,
        )
