from factory.alchemy import SQLAlchemyModelFactory
from auth.models.user import User

from shared.engine import session

import bcrypt


class DefaultAdminUserFactory(SQLAlchemyModelFactory):

    class Meta:
        model = User
        sqlalchemy_session = session
        sqlalchemy_session_persistence = 'commit'
        sqlalchemy_get_or_create = ('alias',)

    alias = "admin"
    first_name = "Administrador"
    email = "admin@pyticket.com"
    role_code = "ADM"
    password = bcrypt.hashpw(b"root", bcrypt.gensalt(16)).decode('utf-8')


