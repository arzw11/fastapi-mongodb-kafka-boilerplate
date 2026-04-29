from fastapi import FastAPI
from application.api.messages.handlers import router as message_router


def create_app() -> FastAPI:
    app = FastAPI(
        title='Kafka Chat',
        docs_url='/api/docs',
        description='Шаблон чата + Kafka',
        debug=True,
    )
    app.include_router(message_router, prefix='/chats')
    return app
