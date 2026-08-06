import enum

from pydantic_settings import BaseSettings


class Environment(str, enum.Enum):
    DEV = "dev"
    PROD = "prod"
    LOCAL = "local"


class GeneralSettings(BaseSettings):
    API_PORT: int
    ENVIRONMENT: Environment = Environment.DEV
