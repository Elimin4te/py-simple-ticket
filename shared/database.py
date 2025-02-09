from sqlalchemy import null, Boolean, String, DateTime, Integer
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, validates

from datetime import datetime

from typing import Optional, TypeAlias

from configuration.settings import TIMEZONE

from shared.validators import (
    code_validator, 
    name_validator
)

# Common Types
NULL = null()

CommonString: TypeAlias = Mapped[str]
NullableString: TypeAlias = Mapped[Optional[str]]

CommonDatetime: TypeAlias = Mapped[datetime]
NullableDatetime: TypeAlias = Mapped[Optional[datetime]]

Id: TypeAlias = Mapped[int]

# Common Mapping Shortcuts

common_datetime = lambda timezone_aware=True, default=datetime.now(tz=TIMEZONE), **column_kwargs: mapped_column(
    DateTime(timezone=timezone_aware),
    default=default,
    **column_kwargs
)
""" Generic function for a common datetime field, declaration syntax must be as follows:
``` python
date_field: CommonDatetime = common_datetime()
```
"""

nullable_datetime = lambda timezone_aware=True, default=NULL, **column_kwargs: mapped_column(
    DateTime(timezone=timezone_aware), 
    default=default,
    **column_kwargs
)
""" Generic function for a nullable datetime field, declaration syntax must be as follows:
``` python
date_field: NullableDatetime = nullable_datetime()
```
"""

common_string = lambda length, **column_kwargs: mapped_column(String(length), **column_kwargs)
""" Generic function for a common string field, declaration syntax must be as follows:
``` python
string_field: CommonString = common_string(256)
```
"""

nullable_string = lambda length, **column_kwargs: mapped_column(
    String(length), 
    default=NULL, 
    **column_kwargs
)
""" Generic function for a nullable datetime field, declaration syntax must be as follows:
``` python
string_field: NullableString = nullable_string(256)
```
"""

generic_id = lambda  auto_increment=True, **column_kwargs: mapped_column(
    Integer,
    primary_key=True,
    autoincrement=auto_increment,
    **column_kwargs
)
""" Generic function for an integer id field, declaration syntax must be as follows:
``` python
id: Id = generic_id('id')
```
"""


class Base(DeclarativeBase):
    """ Inheritable SQLAlchemy Declarative Base. """


class IsActiveMixin():
    """ Inheritable for instances that can be logically deleted. """
    BO_activo: Mapped[bool] = mapped_column(Boolean, default=True)


def get_common_entity_mixin(code_length: int = 4, name_length: int = 16, description_length: int = 128):
    """ Fabric the common entity class to be inherited with parametizable field lengths. """

    class CommonEntityMixin():
        """ Inheritable for instances that have the common code, name and description attribute definition. """

        AF_codigo: Mapped[str] = mapped_column(String(code_length), primary_key=True) 
        AF_nombre: Mapped[str] = mapped_column(String(name_length))
        AF_descripcion: Mapped[str] = mapped_column(String(description_length))

        @validates('AF_codigo')
        def validate_code(self, key, value):
            return code_validator(value)

        @validates('AF_nombre')
        def validate_code(self, key, value):
            return name_validator(value)
    
    return CommonEntityMixin


class ArchivableMixin():
    """ Inheritable for instances that can be archived (tickets, incidences). """

    BO_archivado: Mapped[bool] = mapped_column(Boolean, default=False)
    AF_motivo_archivado: NullableString = nullable_string(256)
    AF_fecha_archivado: NullableDatetime = nullable_datetime()


