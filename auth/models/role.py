from shared.database import Base, get_common_entity_mixin, IsActiveMixin

_Common = get_common_entity_mixin()

class Role(Base, _Common, IsActiveMixin):   
    __tablename__ = 'Roles'