from dataclasses import dataclass

from service_layer.exceptions.base import ServiceException


@dataclass(eq=False)
class ChatWithThatTitleAlreadyExistsException(ServiceException):
    title: str

    @property
    def message(self) -> str:
        return f'Чат с таким названием "{self.title}" уже существует.'


@dataclass(eq=False)
class ChatNotFoundException(ServiceException):
    chat_oid: str

    @property
    def message(self) -> str:
        return 'Чат с таким ID не существует.'
