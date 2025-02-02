from sqlalchemy import ForeignKey, Integer

from sqlalchemy.orm import (
    Mapped, 
    mapped_column, 
    relationship, 
    backref
)

from shared.database import (
    Base, 
    get_common_entity_mixin, 
    IsActiveMixin, 
    NullableString, 
    NULL
)

# Code, Name, Description generic entity
_Common = get_common_entity_mixin(code_length=8, name_length=64)


class Category(Base, _Common, IsActiveMixin):

    __tablename__ = 'Categories'

    hierarchy_level: Mapped[int] = mapped_column(
        Integer,
        default=0,
        name="NU_nivel_jerarquia"
    )

    # Self Related

    parent_category_code: NullableString = mapped_column(
        ForeignKey('Categorias.AF_codigo'),
        default=NULL,
        name='AF_codigo_categoria_padre'
    )

    parent_category: Mapped["Category"] = relationship(
        remote_side=[parent_category_code],
        backref=backref("child_categories", lazy='joined')
    )