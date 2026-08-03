from dataclasses import dataclass

from service_layer.exceptions.base import ServiceException


@dataclass(eq=False)
class EventHandlersNotRegisteredException(ServiceException):
    event_type: type

    @property
    def message(self) -> str:
        return f'Не удалось найти обработчики для события: {self.event_type}'


@dataclass(eq=False)
class CommandHandlersNotRegisteredException(ServiceException):
    command_type: type

    @property
    def message(self):
        return f'Не удалось найти обработчики для команды: {self.command_type}'


@dataclass(eq=False)
class QueryHandlerNotRegisteredException(ServiceException):
    query_type: type

    @property
    def message(self):
        return f'Не удалось найти обработчики для запроса: {self.query_type}'
