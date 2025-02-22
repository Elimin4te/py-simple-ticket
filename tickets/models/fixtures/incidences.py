from factory.alchemy import SQLAlchemyModelFactory
from factory.faker import Faker
from tickets.models import Incidencia

from shared.engine import session

class IncidenceFactory(SQLAlchemyModelFactory):

    class Meta:
        model = Incidencia
        sqlalchemy_session = session
        sqlalchemy_session_persistence = 'commit'

    AF_titulo = Faker('sentence')
    AF_descripcion = Faker('text')
    AF_nombre_reportador = Faker('name')
    AF_correo_reportador = Faker('email')