from sqlalchemy import Integer, String

from sqlalchemy.orm import (
    Mapped, 
    mapped_column
)

from shared.database import (
    Base, 
    get_common_entity_mixin
)

# Code, Name, Description generic entity
_Common = get_common_entity_mixin(code_length=16, description_length=128)

# Remove name since it is not needed for this entity
del _Common.name


class Priority(Base, _Common):

    __tablename__ = 'Prioridades'

    hex_colour: Mapped[str] = mapped_column(
        String(16),
        name='AF_color'
    )

    priority: Mapped[int] = mapped_column(
        Integer,
        name='NU_prioridad',
        default=0
    )