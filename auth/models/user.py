from sqlalchemy import Integer, String, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column, relationship, backref

from shared.database import Base, NULL
from configuration.settings import TIMEZONE

from typing import Optional
from datetime import datetime

from auth.models.role import Role


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

    last_name: Mapped[Optional[str]] = mapped_column(
        String(64),
        name="AF_apellido",
        default=NULL
    )

    document_number: Mapped[int] = mapped_column(
        Integer,
        name="NU_cedula",
        default=0,
        unique=True
    )

    email: Mapped[str] = mapped_column(
        String(128),
        name="AF_correo",
        unique=True
    )

    password: Mapped[str] = mapped_column(
        String(256),
        name="AF_contraseña"
    )

    alt_email: Mapped[Optional[str]] = mapped_column(
        String(128), 
        name="AF_correo_alternativo",
        unique=True,
        default=NULL
    )

    home_phone_number: Mapped[Optional[str]] = mapped_column(
        String(16),
        name="AF_telefono_casa",
        default=NULL
    )

    personal_phone_number: Mapped[Optional[str]] = mapped_column(
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
        default=NULL
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        name="BO_activo",
        default=True
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
    supervisor: Mapped[Optional["User"]] = relationship(
        remote_side=[alias], 
        backref=backref('supervises', lazy='joined')
    )

    # Parents
    role: Mapped["Role"] = relationship(
        remote_side=[Role.code],
        backref=backref('users', lazy='joined')
    )
