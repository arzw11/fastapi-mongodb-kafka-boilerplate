from punq import Container, Scope

from infrastructure.repositories.base import BaseChatRepository
from infrastructure.repositories.memory import MemoryChatRepository
from project.containers import _init_container


def init_dummy_container() -> Container:
    container: Container = _init_container()

    container.register(
        service=BaseChatRepository,
        factory=MemoryChatRepository,
        scope=Scope.singleton,
    )

    return container
