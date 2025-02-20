from sqlalchemy import ForeignKey
from sqlalchemy.orm import (
    mapped_column
)

from shared.database import (
    Base, 
    Id, generic_id
)

class DocumentRelatedMixin:

    NU_id: Id = generic_id()
    NU_id_documento: Id = mapped_column(ForeignKey('DocumentosAdjuntos.NU_id'))


class ArchivoAdjuntoIncidencia(Base, DocumentRelatedMixin):

    __tablename__ = "ArchivosAdjuntosIncidencias"
    NU_incidencia: Id = mapped_column(ForeignKey('Incidencias.NU_incidencia'))


class ArchivoAdjuntoTicket(Base, DocumentRelatedMixin):

    __tablename__ = "ArchivosAdjuntosTickets"
    NU_ticket: Id = mapped_column(ForeignKey('Tickets.NU_ticket'))


class ArchivoAdjuntoTraza(Base, DocumentRelatedMixin):

    __tablename__ = "ArchivosAdjuntosTrazas"
    NU_traza: Id = mapped_column(ForeignKey('TrazaDeTickets.NU_traza'))
