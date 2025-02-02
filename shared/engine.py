from configuration.settings import settings

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

ENGINE = create_engine(settings.get_database_url(), echo=settings.ENGINE_ECHO)
session = Session(ENGINE)