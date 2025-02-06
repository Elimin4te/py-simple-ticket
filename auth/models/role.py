from shared.database import Base, IsActiveMixin, get_common_entity_mixin

_Common = get_common_entity_mixin()

class Rol(Base, _Common, IsActiveMixin):   
    __tablename__ = 'Roles'