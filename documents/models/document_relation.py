from sqlalchemy import ForeignKey
from sqlalchemy.orm import (
    Mapped, 
    mapped_column, 
    relationship, 
    backref
)

from shared.database import (
    Base, 
    Id, generic_id,
    NullableString, nullable_string,  
    CommonString, common_string, 
    CommonDatetime, common_datetime
)

from tickets.models import Incidencia, Ticket, TrazaDeTicket


common_linked_document_backref = backref('documentos_adjuntos', lazy='joined')


class DocumentRelatedMixin:

    id: Id = generic_id()
    NU_id_documento: Id = mapped_column(ForeignKey('DocumentosAdjuntos.id'))


class ArchivoAdjuntoIncidencia(Base, DocumentRelatedMixin):

    __tablename__ = "ArchivosAdjuntosIncidencias"

    NU_incidencia: Id = mapped_column(ForeignKey('Incidencias.NU_incidencia'))
    incidencia: Mapped[Incidencia] = relationship(
        remote_side=[Incidencia.NU_incidencia],
        backref=common_linked_document_backref
    )


class ArchivoAdjuntoTicket(Base, DocumentRelatedMixin):

    __tablename__ = "ArchivosAdjuntosTickets"

    NU_ticket: Id = mapped_column(ForeignKey('Tickets.NU_ticket'))
    incidencia: Mapped[Ticket] = relationship(
        remote_side=[Ticket.NU_ticket],
        backref=common_linked_document_backref
    )


class ArchivoAdjuntoTraza(Base, DocumentRelatedMixin):

    __tablename__ = "ArchivosAdjuntosTrazas"

    NU_traza: Id = mapped_column(ForeignKey('TrazaDeTickets.NU_traza'))
    incidencia: Mapped[TrazaDeTicket] = relationship(
        remote_side=[TrazaDeTicket.NU_traza],
        backref=common_linked_document_backref
    )