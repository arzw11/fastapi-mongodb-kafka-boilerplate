from fastapi import APIRouter, Depends, HTTPException, status

from punq import Container

from application.api.messages.schemas import CreateChatInSchema, CreateChatOutSchema
from application.api.schemas import ErrorSchema
from domain.exceptions.base import ApplicationException
from project.containers import get_container
from service_layer.commands.messages import CreateChatCommand
from service_layer.mediator import Mediator


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
