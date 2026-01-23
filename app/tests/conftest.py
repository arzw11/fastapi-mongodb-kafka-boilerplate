import pytest

from infrastructure.repositories.base import (
    BaseChatRepository,
    MemoryChatRepository,
)
from service_layer.init import init_mediator
from service_layer.mediator import Mediator


@pytest.fixture(scope='package')
def chat_repository() -> MemoryChatRepository:
    return MemoryChatRepository()


@pytest.fixture(scope='package')
def mediator(chat_repository: BaseChatRepository) -> Mediator:
    mediator = Mediator()
    init_mediator(mediator=mediator, chat_repository=chat_repository)

    return mediator
