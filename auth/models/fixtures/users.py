from factory.alchemy import SQLAlchemyModelFactory
from auth.models.user import User

import bcrypt


class AdminUserFactory(SQLAlchemyModelFactory):

    class Meta:
        model = User

    alias = "admin"
    first_name = "Administrador"
    email = "admin@pyticket.com"
    role_code = "ADM"
    password = bcrypt.hashpw(b"root", bcrypt.gensalt(16))


