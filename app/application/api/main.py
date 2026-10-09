
from contextlib import asynccontextmanager

from fastapi import FastAPI

from application.api.lifespan import (
    start_kafka,
    stop_kafka,
)
from application.api.messages.handlers import router as message_router
from project.configs import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    await start_kafka()

    yield

    await stop_kafka()


def create_app() -> FastAPI:
    settings.config_logger()

    app = FastAPI(
        title='Kafka Chat',
        docs_url='/api/docs',
        description='Шаблон чата + Kafka',
        lifespan=lifespan,
        debug=True,
    )
    app.include_router(message_router, prefix='/chats')
    return app
