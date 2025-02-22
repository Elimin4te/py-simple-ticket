from sqlalchemy import Integer, String

from sqlalchemy.orm import (
    Mapped, 
    mapped_column,
    validates
)

from shared.database import (
    Base, 
    CommonString, common_string,
    code_validator
)


class Prioridad(Base):

    __tablename__ = 'Prioridades'

    AF_codigo: Mapped[str] = mapped_column(String(16), primary_key=True) 
    AF_descripcion: Mapped[str] = mapped_column(String(128))

    AF_color: CommonString = common_string(16, unique=True)
    NU_prioridad: Mapped[int] = mapped_column(Integer, default=0, unique=True)

    @validates('NU_prioridad')
    def validate_priority(self, key, value):
        assert 1000 > value > 0, "La prioridad debe ser al menos de 1 y máximo de 999." 
        return value

    @validates('AF_codigo')
    def validate_code(self, key, value):
        return code_validator(value)
