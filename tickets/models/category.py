from sqlalchemy import ForeignKey, Integer

from sqlalchemy.orm import (
    Mapped, 
    mapped_column, 
    relationship, 
    backref,
    validates
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


class Categoria(Base, _Common, IsActiveMixin):

    __tablename__ = 'Categorias'

    NU_nivel_jerarquia: Mapped[int] = mapped_column(Integer, default=0)

    # Self Related

    AF_codigo_categoria_padre: NullableString = mapped_column(ForeignKey('Categorias.AF_codigo'), default=NULL)
    categoria_padre: Mapped["Categoria"] = relationship(
        remote_side="Categoria.AF_codigo",
        backref=backref("categorias_hijas", lazy='joined')
    )

    @validates('NU_nivel_jerarquia')
    def validate_hierarchy(self, key, value):
        assert 10 > value > 0, "El nivel de jerarquía debe ser al menos de 1 y máximo de 9." 
        return value
        