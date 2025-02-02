from factory.alchemy import SQLAlchemyModelFactory
from auth.models.role import Role


class SupervisorRoleFactory(SQLAlchemyModelFactory):

    class Meta:
        model = Role

    code = 'SPVS'
    name = 'Supervisor'
    description = 'Supervisan a los analistas de soporte, pueden crear y asignar tickets, además de ver reportes.'
    is_active = True


class SupportRoleFactory(SQLAlchemyModelFactory):

    class Meta:
        model = Role

    code = 'ASPR'
    name = 'Analista'
    description = 'Ven sus tickets asignados, los resuelven y crean trazas.'
    is_active = True


class AdminRoleFactory(SQLAlchemyModelFactory):

    class Meta:
        model = Role

    code = 'ADM'
    name = 'Administrador'
    description = 'Pueden realizar las funciones del supervisor y las del analista, además puede crear nuevos usuarios.'
    is_active = True
