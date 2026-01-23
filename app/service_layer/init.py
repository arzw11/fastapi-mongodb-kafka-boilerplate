from infrastructure.repositories.base import BaseChatRepository
from service_layer.commands.messages import (
    CreateChatCommand,
    CreateChatCommandHandler,
)
from service_layer.mediator import Mediator


def init_mediator(
    mediator: Mediator,
    chat_repository: BaseChatRepository,
):
    mediator.register_command(
        CreateChatCommand,
        [CreateChatCommandHandler(chat_repository=chat_repository)],
    )
