from pydantic import Field
from pydantic_settings import BaseSettings


class KafkaSettings(BaseSettings):
    KAFKA_PORT: int
    KAFKA_URI: str
    KAFKA_NEW_CHATS_TOPIC: str = Field(default='new-chats-topic')

    @property
    def kafka_url(self) -> str:
        return f'{self.KAFKA_URI}:{self.KAFKA_PORT}'
