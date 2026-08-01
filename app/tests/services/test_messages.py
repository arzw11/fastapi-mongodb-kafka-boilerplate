import pytest
from faker import Faker

from domain.entities.messages import Chat
from domain.values.messages import Title
from infrastructure.repositories.messages.base import BaseChatsRepository
from service_layer.commands.messages import CreateChatCommand
from service_layer.exceptions.messages import ChatWithThatTitleAlreadyExistsException
from service_layer.mediator import Mediator


@pytest.mark.asyncio
async def test_create_chat_command_success(
    chat_repository: BaseChatsRepository,
    mediator: Mediator,
    faker: Faker,
):
    chat, *_ = await mediator.handle_command(CreateChatCommand(title=faker.text()))
    print(chat)

    assert await chat_repository.check_chat_exists_by_title(title=chat.title.as_generic_type()), f'{chat=}'


@pytest.mark.asyncio
async def test_create_chat_command_title_already_exists(
    chat_repository: BaseChatsRepository,
    mediator: Mediator,
    faker: Faker,
):
    title_text = faker.text()
    chat = Chat(title=Title(title_text))
    await chat_repository.add_chat(chat)

    assert chat in chat_repository._chats

    with pytest.raises(ChatWithThatTitleAlreadyExistsException):
        await mediator.handle_command(CreateChatCommand(title=title_text))

    assert len(chat_repository._chats) == 1
