from collections import defaultdict
from dataclasses import (
    dataclass,
    field,
)
from typing import Iterable

from domain.events.base import BaseEvent
from service_layer.commands.base import (
    BaseCommand,
    CommandHandler,
    CR,
    CT,
)
from service_layer.events.base import (
    ER,
    ET,
    EventHandler,
)
from service_layer.exceptions.mediator import (
    CommandHandlersNotRegisteredException,
    QueryHandlerNotRegisteredException,
)
from service_layer.mediator.command import CommandMediator
from service_layer.mediator.event import EventMediator
from service_layer.mediator.query import QueryMediator
from service_layer.queries.base import (
    BaseQuery,
    QR,
    QT,
    QueryHandler,
)


@dataclass(eq=False)
class Mediator(CommandMediator, EventMediator, QueryMediator):
    events_map: dict[ET, list[EventHandler]] = field(
        default_factory=lambda: defaultdict(list),
        kw_only=True,
    )
    commands_map: dict[CT, list[CommandHandler]] = field(
        default_factory=lambda: defaultdict(list),
        kw_only=True,
    )
    queries_map: dict[QT, QueryHandler] = field(
        default_factory=dict,
        kw_only=True,
    )

    def register_event(self, event: ET, event_handlers: Iterable[EventHandler[ET, ER]]):
        self.events_map[event].extend(event_handlers)

    def register_command(self, command: CT, command_handlers: Iterable[CommandHandler[CT, CR]]):
        self.commands_map[command].extend(command_handlers)

    def register_query(self, query: QT, query_handler: QueryHandler[QT, QR]):
        self.queries_map[query] = query_handler

    async def publish(self, events: Iterable[BaseEvent]) -> Iterable[ER]:
        result = []

        for event in events:
            handlers: Iterable[EventHandler] = self.events_map[event.__class__]
            result.extend([await handler.handle(event) for handler in handlers])

        return result

    async def handle_command(self, command: BaseCommand) -> Iterable[CR]:
        command_type = command.__class__
        handlers = self.commands_map.get(command_type)

        if not handlers:
            raise CommandHandlersNotRegisteredException(command_type=command_type)

        return [await handler.handle(command) for handler in handlers]

    async def handle_query(self, query: BaseQuery) -> QR:
        query_type = query.__class__
        handler = self.queries_map.get(query_type)

        if handler is None:
            raise QueryHandlerNotRegisteredException(query_type=query_type)

        return await handler.handle(query)
