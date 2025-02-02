from sqlalchemy import String, Integer, DateTime
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from datetime import datetime

from configuration.settings import TIMEZONE
from shared.database import Base, ArchivableMixin, Id, generic_id


class Incidence(Base, ArchivableMixin):

    __tablename__ = 'Incidencias'

    id: Id = generic_id('NU_incidencia')

    title: Mapped[str] = mapped_column(
        String(128),
        name = 'AF_titulo'
    )

    description: Mapped[str] = mapped_column(
        String(5096),
        name = 'AF_description'
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        name="AF_fecha_creacion",
        default=datetime.now(tz=TIMEZONE)
    )

    reporting_user_name: Mapped[str] = mapped_column(
        String(128),
        name='AF_nombre_reportador'
    )

    reporting_user_email: Mapped[str] = mapped_column(
        String(128),
        name='AF_correo_reportador'
    )

