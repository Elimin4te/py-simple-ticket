from shared.database import Base
from configuration.settings import settings
from sqlalchemy import create_engine

ENGINE = create_engine(settings.get_database_url(), echo=settings.ENGINE_ECHO)
