from pydantic import ConfigDict

from project.configs.general import GeneralSettings
from project.configs.mongo import MongoSettings


class Settings(
    GeneralSettings,
    MongoSettings,
):
    model_config = ConfigDict(
        case_sensitive=True,
        env_file='.env',
    )


settings = Settings()
