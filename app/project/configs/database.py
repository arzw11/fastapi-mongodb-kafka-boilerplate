from pydantic import Field
from pydantic_settings import BaseSettings


class MongoSettings(BaseSettings):
    MONGO_DB_CONNECTION_URI: str
    MONGO_DB_ADMIN_USERNAME: str
    MONGO_DB_ADMIN_PASSWORD: str

    MONGODB_CHAT_DATABASE: str = Field(default='chat')
    MONGODB_CHAT_COLLECTION: str = Field(default='chat')
    MONGODB_MESSAGES_COLLECTION: str = Field(default='messages')
