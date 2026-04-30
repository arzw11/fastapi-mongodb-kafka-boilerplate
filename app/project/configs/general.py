from pydantic_settings import BaseSettings


class GeneralSettings(BaseSettings):
    API_PORT: int
