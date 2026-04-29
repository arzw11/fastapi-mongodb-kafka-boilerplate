from functools import lru_cache

from punq import Container, Scope

from infrastructure.repositories.base import BaseChatRepository
from infrastructure.repositories.memory import MemoryChatRepository
from service_layer.commands.messages import (
    CreateChatCommand,
    CreateChatCommandHandler,
)
from service_layer.mediator import Mediator


@lru_cache(1)
def get_container() -> Container:
    return _init_container()


def _init_container() -> Container:
    container: Container = Container()

    container.register(
        service=BaseChatRepository,
        factory=MemoryChatRepository,
        scope=Scope.singleton,
    )
    container.register(CreateChatCommandHandler)

    def init_mediator() -> Mediator:
        mediator: Mediator = Mediator()

        mediator.register_command(
            CreateChatCommand,
            [CreateChatCommandHandler(chat_repository=container.resolve(BaseChatRepository))],
        )

        return mediator

    container.register(Mediator, init_mediator)

    return container
