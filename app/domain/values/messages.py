from dataclasses import dataclass

from domain.exceptions.messages import (
    EmptyTextException,
    EmptyTitleException,
    TitleTooLongException,
)
from domain.values.base import BaseValueObject


@dataclass(frozen=True)
class Text(BaseValueObject[str]):
    def validate(self):
        if not self.value:
            raise EmptyTextException()

    def as_generic_type(self) -> str:
        return str(self.value)


@dataclass(frozen=True)
class Title(BaseValueObject[str]):
    def validate(self):
        if not self.value:
            raise EmptyTitleException()

        if len(self.value) > 255:
            raise TitleTooLongException(text=self.value)

    def as_generic_type(self) -> str:
        return str(self.value)
