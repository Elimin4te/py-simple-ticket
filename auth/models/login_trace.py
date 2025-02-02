from sqlalchemy import Integer, DateTime, ForeignKey
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column, relationship

from shared.database import Base
from configuration.settings import TIMEZONE

from typing import TYPE_CHECKING

from datetime import datetime

if TYPE_CHECKING:
    from auth.models.user import User

class LoginTrace(Base):

    __tablename__ = "IniciosDeSesion"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
        name="NU_numero"
    )

    user_alias: Mapped[int] = mapped_column(
        ForeignKey("Usuarios.AF_alias"),
        name="AF_usuario"
    )

    started_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        name="TI_fecha_inicio",
        default=datetime.now(tz=TIMEZONE)
    )

    finished_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        name="TI_fecha_fin",
    )

    # Parents
    user: Mapped["User"] = relationship(back_populates="login_traces")