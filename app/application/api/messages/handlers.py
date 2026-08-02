from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)

from punq import Container

from application.api.messages.schemas import (
    ChatDetailSchema,
    CreateChatInSchema,
    CreateChatOutSchema,
    CreateMessageResponseSchema,
    CreateMessageSchema,
)
from application.api.schemas import ErrorSchema
from domain.exceptions.base import ApplicationException
from project.containers import get_container
from service_layer.commands.messages import (
    CreateChatCommand,
    CreateMessageCommand,
)
from service_layer.mediator import Mediator
from service_layer.queries.messages import GetChatDetailQuery


router = APIRouter(tags=['Chats'])


@router.post(
    '',
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_201_CREATED: {'model': CreateChatOutSchema},
        status.HTTP_400_BAD_REQUEST: {'model': ErrorSchema},
    },
    description='Эндпоинт создаёт новый чат, если чат с таким названием существует, то возвращается 400 ошибка',
)
async def create_chat_handler(
    schema: CreateChatInSchema,
    container: Container = Depends(get_container),
):
    mediator: Mediator = container.resolve(Mediator)

    try:
        chat, *_ = await mediator.handle_command(CreateChatCommand(title=schema.title))

    except ApplicationException as exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=exception.message,
        )

    return CreateChatOutSchema.from_entity(chat)


@router.post(
    '/{chat_oid}/messages',
    status_code=status.HTTP_201_CREATED,
    description='Эндпоинт на добавление нового сообщения в чат с переданным ObjectID',
    responses={
        status.HTTP_201_CREATED: {'model': CreateMessageSchema},
        status.HTTP_400_BAD_REQUEST: {'model': ErrorSchema},
    },
)
async def create_message_handler(
    chat_oid: str,
    schema: CreateMessageSchema,
    container: Container = Depends(get_container),
) -> CreateMessageResponseSchema:
    mediator: Mediator = container.resolve(Mediator)

    try:
        message, *_ = await mediator.handle_command(
            CreateMessageCommand(
                text=schema.text,
                chat_oid=chat_oid,
            ),
        )

    except ApplicationException as exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={'error': exception.message},
        )

    return CreateMessageResponseSchema.from_entity(message)


@router.get(
    '/{chat_oid}/',
    status_code=status.HTTP_200_OK,
    description='Получить информацию о чате и все сообщения в нём.',
    responses={
        status.HTTP_200_OK: {'model': ChatDetailSchema},
        status.HTTP_400_BAD_REQUEST: {'model': ErrorSchema},
    },
)
async def get_messages_w_chat_handler(
    chat_oid: str,
    container: Container = Depends(get_container),
) -> ChatDetailSchema:
    mediator: Mediator = container.resolve(Mediator)

    try:
        chat, *_ = await mediator.handle_query(GetChatDetailQuery(chat_oid=chat_oid))

    except ApplicationException as exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={'error': exception.message},
        )

    return ChatDetailSchema.from_entity(chat=chat)
