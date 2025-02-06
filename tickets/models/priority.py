from sqlalchemy import Integer

from sqlalchemy.orm import (
    Mapped, 
    mapped_column
)

from shared.database import (
    Base, 
    get_common_entity_mixin,
    CommonString, common_string
)

# Code, Name, Description generic entity
_Common = get_common_entity_mixin(code_length=16, description_length=128)

# Remove name since it is not needed for this entity
del _Common.name


class Prioridad(Base, _Common):

    __tablename__ = 'Prioridades'

    AF_color: CommonString = common_string(16)
    NU_prioridad: Mapped[int] = mapped_column(Integer, default=0)