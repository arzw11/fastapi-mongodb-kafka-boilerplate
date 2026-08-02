from dataclasses import dataclass

from domain.entities.messages import Chat
from infrastructure.repositories.messages.base import BaseChatsRepository
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
