from factory.alchemy import SQLAlchemyModelFactory
from auth.models.role import Role
from shared.engine import session

class RoleFactory(SQLAlchemyModelFactory):

    class Meta:
        model = Role
        sqlalchemy_session = session
        sqlalchemy_session_persistence = 'commit'
        sqlalchemy_get_or_create = ('code',)

class SupervisorRoleFactory(RoleFactory):

    code = 'SPVS'
    name = 'Supervisor'
    description = 'Supervisan a los analistas de soporte, pueden crear y asignar tickets, además de ver reportes.'
    is_active = True


class SupportRoleFactory(RoleFactory):

    code = 'ASPR'
    name = 'Analista'
    description = 'Ven sus tickets asignados, los resuelven y crean trazas.'
    is_active = True


class AdminRoleFactory(RoleFactory):

    code = 'ADM'
    name = 'Administrador'
    description = 'Pueden realizar las funciones del supervisor y las del analista, además puede crear nuevos usuarios.'
    is_active = True
