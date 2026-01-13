from dataclasses import dataclass

from domain.exceptions.base import ApplicationException


@dataclass(eq=False)
class EmptyTextException(ApplicationException):
    @property
    def message(self) -> str:
        return 'Текст не может быть пустым.'


@dataclass(eq=False)
class EmptyTitleException(ApplicationException):
    @property
    def message(self) -> str:
        return 'Название не может быть пустым.'


@dataclass(eq=False)
class TitleTooLongException(ApplicationException):
    text: str

    @property
    def message(self) -> str:
        return f'Слишком длинное название "{self.text[:255]}"'
