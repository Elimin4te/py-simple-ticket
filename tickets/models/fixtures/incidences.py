from factory.alchemy import SQLAlchemyModelFactory
from factory.faker import Faker
from tickets.models import Incidencia

from shared.engine import session

class IncidenceFactory(SQLAlchemyModelFactory):

    class Meta:
        model = Incidencia
        sqlalchemy_session = session
        sqlalchemy_session_persistence = 'commit'

    AF_titulo = Faker('sentence', locale='es_MX')
    AF_descripcion = Faker('text', locale='es_MX')
    AF_nombre_reportador = Faker('name', locale='es_MX')
    AF_correo_reportador = Faker('email', locale='es_MX')