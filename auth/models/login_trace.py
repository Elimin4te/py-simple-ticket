from sqlalchemy import Integer, DateTime, ForeignKey
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column, relationship, backref

from shared.database import Base, NULL, NullableDatetime, nullable_datetime, Id, generic_id
from configuration.settings import TIMEZONE

from datetime import datetime

from auth.models.user import User


class LoginTrace(Base):

    __tablename__ = "IniciosDeSesion"

    id: Id = generic_id("NU_numero")

    user_alias: Mapped[str] = mapped_column(
        ForeignKey("Usuarios.AF_alias"),
        name="AF_usuario"
    )

    started_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        name="TI_fecha_inicio",
        default=datetime.now(tz=TIMEZONE)
    )

    finished_at: NullableDatetime = nullable_datetime('TI_fecha_fin')

    # Parents
    user: Mapped["User"] = relationship(
        remote_side=[User.alias],
        backref=backref('login_traces', lazy='joined')
    )