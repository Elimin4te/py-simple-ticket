from sqlalchemy import null
from sqlalchemy.orm import DeclarativeBase
from pytz import timezone

NULL = null()

class Base(DeclarativeBase):
    pass

TIMEZONE = timezone('America/Caracas')