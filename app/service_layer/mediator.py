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
    EventHandlersNotRegisteredException,
    QueryHandlerNotRegisteredException,
)
from service_layer.queries.base import (
    BaseQuery,
    QR,
    QT,
    QueryHandler,
)


@dataclass(eq=False)
class Mediator:
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
        self.events_map[event].append(event_handlers)

    def register_command(self, command: CT, command_handlers: Iterable[CommandHandler[CT, CR]]):
        self.commands_map[command].extend(command_handlers)

    def register_query(self, query: QT, query_handler: QueryHandler[QT, QR]):
        self.queries_map[query] = query_handler

    async def publish(self, events: Iterable[BaseEvent]) -> Iterable[ER]:
        event_type = events.__class__
        handlers = self.events_map.get(event_type)

        if not handlers:
            raise EventHandlersNotRegisteredException(event_type=event_type)

        result = []
        for event in events:
            result.extend([await handler.handle(event) for handler in handlers])

        return [await handler.handle(event) for handler in handlers]

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
