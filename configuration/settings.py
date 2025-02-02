from pydantic_settings import BaseSettings
from pytz import timezone

class Settings(BaseSettings):
    """Base Setting."""

    PROJECT_NAME: str = "PyTicket"
    PROJECT_VERSION: str = "0.0.1"
    TIMEZONE: str = 'America/Caracas'

    DATABASE_ENGINE: str
    DATABASE_HOST: str
    DATABASE_PORT: str
    DATABASE_NAME: str
    DATABASE_USER: str
    DATABASE_PASSWORD: str

    class Config:
        env_file = ".env"

    def get_timezone(self):
        return timezone(self.TIMEZONE)

    def get_database_url(self) -> str:
        return (
            f"{self.DATABASE_ENGINE.lower()}://{self.DATABASE_USER}:{self.DATABASE_PASSWORD}@{self.DATABASE_HOST}:{self.DATABASE_PORT}/{self.DATABASE_NAME}"
        )

settings = Settings()
TIMEZONE = settings.get_timezone()
