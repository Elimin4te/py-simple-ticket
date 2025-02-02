from sqlalchemy import Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column, relationship

from app.utils.globals import Base, NULL, TIMEZONE

from typing import Optional, TYPE_CHECKING

from datetime import datetime

if TYPE_CHECKING:
    from app.auth.models.role import Role
    from app.auth.models.login_trace import LoginTrace
    from app.auth.models.action_trace import ActionTrace


class User(Base):

    __tablename__ = "Usuarios"

    alias: Mapped[str] = mapped_column(
        String(16),
        primary_key=True, 
        name="AF_alias"
    )

    first_name: Mapped[str] = mapped_column(
        String(64),
        name="AF_nombre"
    )

    last_name: Mapped[str] = mapped_column(
        String(64),
        name="AF_apellido"
    )

    document_number: Mapped[int] = mapped_column(
        Integer,
        name="NU_cedula"
    )

    email: Mapped[str] = mapped_column(
        String(128),
        name="AF_correo"
    )

    password: Mapped[str] = mapped_column(
        String(256),
        name="AF_contraseña"
    )

    alt_email: Mapped[Optional[str]] = mapped_column(
        String(128), 
        name="AF_correo_alternativo",
        default=NULL
    )

    home_phone_number: Mapped[Optional[str]] = mapped_column(
        String(16),
        name="AF_telefono_casa",
        default=NULL
    )

    personal_phone_number: Mapped[str] = mapped_column(
        String(16),
        name="AF_telefono_personal"
    )

    joined_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        name="TI_fecha_ingreso",
        default=datetime.now(tz=TIMEZONE)
    )

    last_login_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        name="TI_ultimo_inicio_sesion",
        default=datetime.now(tz=TIMEZONE)
    )

    role_code: Mapped[str] = mapped_column(
        ForeignKey('Roles.AF_codigo'),
        name='AF_codigo_rol'
    )

    supervisor_code: Mapped[Optional[str]] = mapped_column(
        ForeignKey('Usuarios.AF_alias'),
        name='AF_usuario_supervisor',
        default=NULL
    )

    # Self-related
    supervises: Mapped[list["User"]] = relationship(back_populates="supervisor")
    supervisor: Mapped[Optional["User"]] = relationship(back_populates="supervises")

    # Parents
    role: Mapped["Role"] = relationship(back_populates="users")

    # Childrens
    login_traces: Mapped[list["LoginTrace"]] = relationship(back_populates="user")
    action_traces: Mapped[list["ActionTrace"]] = relationship(back_populates="user")