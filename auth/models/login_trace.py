from sqlalchemy import ForeignKey
from sqlalchemy.orm import (
    Mapped, 
    mapped_column, 
    relationship, 
    backref,
    validates
)

from shared.database import (
    Base,
    Id, generic_id,
    CommonDatetime, common_datetime,
    CommonString,
    NullableDatetime, nullable_datetime
)

from auth.models.user import Usuario


class InicioDeSesion(Base):

    __tablename__ = "IniciosDeSesion"

    NU_numero: Id = generic_id()
    AF_usuario: CommonString = mapped_column(ForeignKey("Usuarios.AF_alias"))
    TI_fecha_inicio: CommonDatetime = common_datetime()
    TI_fecha_fin: NullableDatetime = nullable_datetime()

    # Parents
    usuario: Mapped["Usuario"] = relationship(
        remote_side=[Usuario.AF_alias],
        backref=backref('inicios_de_sesion', lazy='joined')
    )