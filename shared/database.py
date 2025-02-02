from sqlalchemy import null
from sqlalchemy.orm import DeclarativeBase 

NULL = null()

class Base(DeclarativeBase):
    pass
