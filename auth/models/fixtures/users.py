from factory import LazyAttribute
from factory.alchemy import SQLAlchemyModelFactory
from factory.faker import Faker
from auth.models import Usuario

from shared.engine import session

import random
import bcrypt

default_password = bcrypt.hashpw(bytes('root', encoding='utf-8'), bcrypt.gensalt(16)).decode('utf-8')

def generate_document():
    return int(random.random()*10_000_000)


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
    AF_contraseña = default_password


class SupervisorUserFactory(SQLAlchemyModelFactory):

    class Meta:
        model = Usuario
        sqlalchemy_session = session
        sqlalchemy_session_persistence = 'commit'
        sqlalchemy_get_or_create = ('AF_alias',)

    AF_alias = Faker("user_name")
    NU_cedula = LazyAttribute(lambda obj: generate_document())
    AF_nombre = Faker("first_name")
    AF_apellido = Faker("last_name")
    AF_correo = Faker("email")
    AF_codigo_rol = "SPVS"
    AF_contraseña = default_password


class AnalistUserFactory(SQLAlchemyModelFactory):

    class Meta:
        model = Usuario
        sqlalchemy_session = session
        sqlalchemy_session_persistence = 'commit'
        sqlalchemy_get_or_create = ('AF_alias',)

    AF_alias = Faker("user_name")
    NU_cedula = LazyAttribute(lambda obj: generate_document())
    AF_nombre = Faker("first_name")
    AF_apellido = Faker("last_name")
    AF_correo = Faker("email")
    AF_codigo_rol = "ASPR"
    AF_contraseña = default_password
    AF_usuario_supervisor = LazyAttribute(lambda obj: SupervisorUserFactory().AF_alias)


