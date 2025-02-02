from sqlalchemy import Integer, DateTime, ForeignKey, Enum, String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column, relationship, backref

from shared.database import Base
from configuration.settings import TIMEZONE

from typing import Optional
from datetime import datetime

from auth.models.user import User


ACTIONS = Enum(
    "Crear",
    "Modificar",
    "Eliminar",
    name="acciones_auditoria",
    create_type=True
)

class ActionTrace(Base):

    __tablename__ = "Auditorias"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
        name="NU_historico"
    )

    table_name: Mapped[str] = mapped_column(
        String(64),
        name="AF_tabla"
    )

    action: Mapped[str] = mapped_column(
        ACTIONS,
        name="AF_accion"
    )

    registry_id: Mapped[str] = mapped_column(
        String(64),
        name="AF_id_registro"
    )

    field_name: Mapped[Optional[str]] = mapped_column(
        String(64),
        name="AF_campo_modificado"
    )

    old_value: Mapped[Optional[str]] = mapped_column(
        String(128),
        name="AF_valor_viejo"
    )

    new_value: Mapped[Optional[str]] = mapped_column(
        String(128),
        name="AF_valor_nuevo"
    )

    executed_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        name="TI_fecha_accion",
        default=datetime.now(tz=TIMEZONE)
    )

    executed_by: Mapped[int] = mapped_column(
        ForeignKey("Usuarios.AF_alias"),
        name="AF_usuario_modificador"
    )

    # Parents
    user: Mapped["User"] = relationship(
        remote_side=[User.alias],
        backref=backref('action_traces', lazy='joined')
    )