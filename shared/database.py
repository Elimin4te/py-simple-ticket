from sqlalchemy import null, Boolean, String, DateTime, Integer
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from datetime import datetime

from typing import Optional, TypeAlias

# Common Types
NULL = null()
NullableString: TypeAlias = Mapped[Optional[str]]
NullableDatetime: TypeAlias = Mapped[Optional[datetime]]
Id: TypeAlias = Mapped[int]

# Common Mapping Shortcuts

nullable_datetime = lambda field_name, timezone_aware=True, **column_kwargs: mapped_column(
    DateTime(timezone=timezone_aware), 
    name=field_name, 
    default=NULL, 
    **column_kwargs
)
""" Generic function for a nullable datetime field, declaration syntax must be as follows:
``` python
date_field: NullableDatetime = nullable_datetime('my_db_field')
```
"""

nullable_string = lambda length, field_name, **column_kwargs: mapped_column(
    String(length), 
    name=field_name, 
    default=NULL, 
    **column_kwargs
)
""" Generic function for a nullable datetime field, declaration syntax must be as follows:
``` python
string_field: NullableString = nullable_string(256, 'my_db_field')
```
"""

generic_id = lambda field_name='id', auto_increment=True, **column_kwargs: mapped_column(
    Integer,
    primary_key=True,
    name=field_name,
    auto_increment=auto_increment,
    **column_kwargs
)
""" Generic function for an integer id field, declaration syntax must be as follows:
``` python
id: Id = generic_id('id')
```
"""

class Base(DeclarativeBase):
    """ Inheritable SQLAlchemy Declarative Base. """

    pass

class IsActiveMixin():
    """ Inheritable for instances that can be logically deleted. """

    is_active: Mapped[bool] = mapped_column(
        Boolean, 
        default=True,
        name='BO_activo'
    )


def get_common_entity_mixin(code_length: int = 4, name_length: int = 16, description_length: int = 128):
    """ Fabric the common entity class to be inherited with parametizable field lengths. """

    class CommonEntityMixin():
        """ Inheritable for instances that have the common code, name and description attribute definition. """

        code: Mapped[str] = mapped_column(
            String(code_length), 
            primary_key=True,
            name='AF_codigo'
        ) 

        name: Mapped[str] = mapped_column(
            String(name_length),
            name='AF_nombre'
        )

        description: Mapped[str] = mapped_column(
            String(description_length),
            name='AF_descripcion'
        )
    
    return CommonEntityMixin


class ArchivableMixin():
    """ Inheritable for instances that can be archived (tickets, incidences). """

    is_archived: Mapped[bool] = mapped_column(
        Boolean, 
        default=False,
        name='BO_archivado'
    )

    archiving_reason: NullableString = nullable_string(256, 'AF_motivo_archivado')

    archived_at: NullableDatetime = nullable_datetime('AF_fecha_archivado')


