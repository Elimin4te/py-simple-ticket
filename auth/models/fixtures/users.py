from factory.alchemy import SQLAlchemyModelFactory
from auth.models import Usuario

from shared.engine import session

import bcrypt


class DefaultAdminUserFactory(SQLAlchemyModelFactory):

    class Meta:
        model = Usuario
        sqlalchemy_session = session
        sqlalchemy_session_persistence = 'commit'
        sqlalchemy_get_or_create = ('AF_alias',)

    AF_alias = "admin"
    AF_nombre = "Administrador"
    AF_correo = "admin@pyticket.com"
    AF_codigo_rol = "ADM"
    AF_contraseña = bcrypt.hashpw(bytes('root', encoding='utf-8'), bcrypt.gensalt(16)).decode('utf-8')


