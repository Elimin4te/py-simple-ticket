from sqlalchemy import Integer, ForeignKey
from sqlalchemy.orm import (
    Mapped, 
    mapped_column, 
    relationship, 
    backref,
    validates
)

from shared.database import (
    Base,
    NULL, TIMEZONE,
    CommonString, common_string,
    NullableString, nullable_string,
    NullableDatetime, nullable_datetime,
    IsActiveMixin
)

from shared.validators import (
    code_validator, 
    name_validator,
    regex_validator,
    length_validator
)

from typing import Optional
from datetime import datetime

from auth.models import Rol


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

    @validates('AF_alias')
    def validate_alias(self, key, value):
        return code_validator(value, "alias")

    @validates('AF_nombre')
    def validate_name(self, key, value):
        return name_validator(value)

    @validates('AF_apellido')
    def validate_name(self, key, value):
        if value:
            return name_validator(value)

    @validates('AF_cedula')
    def validate_document(self, key, value):
        return length_validator(str(value), 7, 8, 'La Cédula')

    @validates('AF_correo', 'AF_correo_alternativo')
    def validate_email(self, key, value):
        key: str = key
        if value:
            return regex_validator(
                value,
                r"\"?([-a-zA-Z0-9.`?{}]+@\w+\.\w+)\"?",
                " ".join(key.split('_')[1:])
            )

    @validates('AF_telefono_personal')
    def validate_phone_number(self, key, value):
        if value:
            return regex_validator(
                value,
                r"^(\+\d{1,3})?[-.\s]?\(?(\d{3})\)?[-.\s]?(\d{3})[-.\s]?(\d{4})$",
                'teléfono personal'
            )
    
    @validates('AF_telefono_casa')
    def validate_home_phone_number(self, key, value):
        if value:
            return regex_validator(
                value,
                r"^0(2\d{3})\d{6}$",
                'teléfono personal'
            )
