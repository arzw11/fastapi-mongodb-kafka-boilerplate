from fastapi import FastAPI


def create_app() -> FastAPI:
    return FastAPI(
        title='Kafka Chat',
        docs_url='/api/docs',
        description='Шаблон чата + Kafka',
        debug=True,
    )
