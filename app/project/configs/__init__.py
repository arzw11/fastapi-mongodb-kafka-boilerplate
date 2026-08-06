from pydantic import ConfigDict

from project.configs.database import MongoSettings
from project.configs.general import GeneralSettings
from project.configs.logger import LoggingSettings
from project.configs.message_broker import KafkaSettings


class Settings(
    LoggingSettings,
    GeneralSettings,
    KafkaSettings,
    MongoSettings,
):
    model_config = ConfigDict(
        case_sensitive=True,
        env_file='.env',
    )


settings = Settings()
