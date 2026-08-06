from pydantic import Field
from pydantic_settings import BaseSettings


class KafkaSettings(BaseSettings):
    KAFKA_URL: str
    KAFKA_NEW_CHATS_TOPIC: str = Field(default='new-chats-topic')
