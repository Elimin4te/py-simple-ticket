from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column, relationship, backref

from shared.database import (
    Base, 
    NULL, 
    NullableString, 
    NullableDatetime, 
    nullable_string, 
    nullable_datetime,
    IsActiveMixin
)

from configuration.settings import TIMEZONE

from typing import Optional
from datetime import datetime

from auth.models.role import Role


class User(Base, IsActiveMixin):

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

    last_name: NullableString = nullable_string(64, 'AF_apellido')

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

    alt_email: NullableString = nullable_string(128, 'AF_correo_alternativo', unique=True)

    home_phone_number: NullableString = nullable_string(16, 'AF_telefono_casa')

    personal_phone_number: NullableString = nullable_string(32, 'AF_telefono_personal')

    joined_at: NullableDatetime = nullable_datetime('TI_fecha_ingreso', default=datetime.now(tz=TIMEZONE))

    last_login_at: NullableDatetime = nullable_datetime('TI_ultimo_inicio_sesion')

    role_code: Mapped[str] = mapped_column(
        ForeignKey('Roles.AF_codigo'),
        name='AF_codigo_rol'
    )

    supervisor_code: NullableString = mapped_column(
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
