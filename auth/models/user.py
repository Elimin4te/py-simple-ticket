from sqlalchemy import Integer, ForeignKey
from sqlalchemy.orm import (
    Mapped, 
    mapped_column, 
    relationship, 
    backref
)

from shared.database import (
    Base,
    NULL, TIMEZONE,
    CommonString, common_string,
    NullableString, nullable_string,
    NullableDatetime, nullable_datetime,
    IsActiveMixin
)

from typing import Optional
from datetime import datetime

from auth.models.role import Rol


class Usuario(Base, IsActiveMixin):

    __tablename__ = "Usuarios"

    AF_alias: CommonString = common_string(16, primary_key=True)
    AF_nombre: CommonString = common_string(64)
    AF_apellido: NullableString = nullable_string(64)
    NU_cedula: Mapped[int] = mapped_column(Integer, default=0, unique=True)
    AF_correo: CommonString = common_string(128, unique=True)
    AF_contraseña: CommonString = common_string(256)
    AF_correo_alternativo: NullableString = nullable_string(128, unique=True)
    AF_telefono_casa: NullableString = nullable_string(16)
    AF_telefono_personal: NullableString = nullable_string(32)
    TI_fecha_ingreso: NullableDatetime = nullable_datetime(default=datetime.now(tz=TIMEZONE))
    TI_ultimo_inicio_sesion: NullableDatetime = nullable_datetime()

    # ------ Role
    AF_codigo_rol: CommonString = mapped_column(ForeignKey('Roles.AF_codigo'))
    rol: Mapped["Rol"] = relationship(
        remote_side=[Rol.AF_codigo],
        backref=backref('users', lazy='joined')
    )

    # ------ User
    AF_usuario_supervisor: NullableString = mapped_column(ForeignKey('Usuarios.AF_alias'), default=NULL)
    supervisor: Mapped[Optional["Usuario"]] = relationship(
        remote_side=[AF_alias], 
        backref=backref('supervisados', lazy='joined')
    )
    
