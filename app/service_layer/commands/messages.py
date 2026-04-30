from dataclasses import dataclass

from domain.entities.messages import Chat
from domain.values.messages import Title
from infrastructure.repositories.messages.base import BaseChatRepository
from service_layer.commands.base import (
    BaseCommand,
    CommandHandler,
)
from service_layer.exceptions.messages import ChatWithThatTitleAlreadyExistsException


@dataclass(frozen=True)
class CreateChatCommand(BaseCommand):
    title: str


@dataclass(frozen=True)
class CreateChatCommandHandler(CommandHandler[CreateChatCommand, Chat]):
    chat_repository: BaseChatRepository

    async def handle(self, command: CreateChatCommand) -> Chat:
        if await self.chat_repository.check_chat_exists_by_title(title=command.title):
            raise ChatWithThatTitleAlreadyExistsException(title=command.title)

        title = Title(value=command.title)

        new_chat = Chat.create_chat(title=title)

        await self.chat_repository.add_chat(chat=new_chat)

        return new_chat
