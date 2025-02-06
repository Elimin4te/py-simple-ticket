from sqlalchemy import ForeignKey, Enum
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column, relationship, backref

from shared.database import (
    Base, 
    Id, generic_id,
    NullableString, nullable_string,  
    CommonString, common_string, 
    CommonDatetime, common_datetime
)

from auth.models.user import Usuario


ACTIONS = Enum(
    "Crear",
    "Modificar",
    "Eliminar",
    name="acciones_auditoria",
    create_type=True
)

class Auditoria(Base):

    __tablename__ = "Auditorias"

    NU_historico: Id = generic_id()
    AF_tabla: CommonString = common_string(64)
    AF_accion: CommonString = mapped_column(ACTIONS)
    AF_id_registro: CommonString = common_string(64)
    AF_campo_modificado: NullableString = nullable_string(64)
    AF_valor_viejo: NullableString = nullable_string(128)
    AF_valor_nuevo: NullableString = nullable_string(128)
    TI_fecha_accion: CommonDatetime = common_datetime()

    # ------ User
    AF_usuario_modificador: CommonString = mapped_column(ForeignKey("Usuarios.AF_alias"))
    usuario: Mapped["Usuario"] = relationship(
        remote_side=[Usuario.AF_alias],
        backref=backref('auditorias', lazy='joined')
    )