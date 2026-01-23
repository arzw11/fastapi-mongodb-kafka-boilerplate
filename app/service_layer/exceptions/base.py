from dataclasses import dataclass

from domain.exceptions.base import ApplicationException


@dataclass(eq=False)
class ServiceException(ApplicationException):
    @property
    def message(self) -> str:
        return 'Произошла ошибка сервиса.'
