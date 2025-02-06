from factory.alchemy import SQLAlchemyModelFactory
from auth.models import Rol
from shared.engine import session

class RoleFactory(SQLAlchemyModelFactory):

    class Meta:
        model = Rol
        sqlalchemy_session = session
        sqlalchemy_session_persistence = 'commit'
        sqlalchemy_get_or_create = ('AF_codigo',)

class SupervisorRoleFactory(RoleFactory):

    AF_codigo = 'SPVS'
    AF_nombre = 'Supervisor'
    AF_descripcion = 'Supervisan a los analistas de soporte, pueden crear y asignar tickets, además de ver reportes.'
    BO_activo = True


class SupportRoleFactory(RoleFactory):

    AF_codigo = 'ASPR'
    AF_nombre = 'Analista'
    AF_descripcion = 'Ven sus tickets asignados, los resuelven y crean trazas.'
    BO_activo = True


class AdminRoleFactory(RoleFactory):

    AF_codigo = 'ADM'
    AF_nombre = 'Administrador'
    AF_descripcion = 'Pueden realizar las funciones del supervisor y las del analista, además puede crear nuevos usuarios.'
    BO_activo = True
