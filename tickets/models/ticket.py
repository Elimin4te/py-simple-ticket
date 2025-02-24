from sqlalchemy import Integer, Enum, ForeignKey, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship, backref

from shared.database import (
    Base,
    ArchivableMixin, 
    NULL, Id, generic_id,
    NullableDatetime, nullable_datetime,
    CommonString, common_string,
    CommonDatetime, common_datetime
)

from documents.models import (
    ArchivoAdjuntoTicket, 
    ArchivoAdjuntoTraza, 
    RelatedDocuments, 
    related_documents
)

from tickets.models import Categoria, Prioridad, Incidencia
from auth.models import Usuario

STATUS_OPTS = [
    "Nuevo",
    "Asignado",
    "En Curso",
    "Resuelto",
    "Cerrado"
]

ESTATUS = Enum(
    *STATUS_OPTS,
    name="estatus_tickets",
    create_type=True
)


class Ticket(Base, ArchivableMixin):

    __tablename__ = 'Tickets'

    NU_ticket: Id = generic_id()
    AF_titulo: CommonString = common_string(128)
    AF_descripcion: CommonString = common_string(5096)
    TI_fecha_asignacion: NullableDatetime = nullable_datetime()
    TI_fecha_resolucion: NullableDatetime = nullable_datetime()
    AF_estatus: CommonString = mapped_column(ESTATUS)

    # Parents

    # ---- Incidence

    NU_incidencia: Mapped[int] = mapped_column(ForeignKey('Incidencias.NU_incidencia'), unique=True)
    incidencia: Mapped[Incidencia] = relationship(
        remote_side=[Incidencia.NU_incidencia],
        backref=backref('ticket', lazy='joined')
    )

    # ---- Category

    AF_codigo_categoria: Mapped[str] = mapped_column(ForeignKey('Categorias.AF_codigo'))
    categoria: Mapped[Categoria] = relationship(
        remote_side=[Categoria.AF_codigo],
        backref=backref('tickets', lazy='joined')
    )

    # ---- Priority

    AF_codigo_prioridad: Mapped[str] = mapped_column(ForeignKey('Prioridades.AF_codigo'))
    prioridad: Mapped[Prioridad] = relationship(
        remote_side=[Prioridad.AF_codigo],
        backref=backref('tickets', lazy='joined')
    )

    # ---- Assigned User

    AF_analista_asignado: Mapped[str] = mapped_column(
        ForeignKey('Usuarios.AF_alias'), default=NULL, nullable=True
    )
    analista_asignado: Mapped[Usuario] = relationship(
        remote_side=[Usuario.AF_alias],
        backref=backref('assigned_tickets', lazy='joined')
    )

    # ---- Attached Files
    documentos_adjuntos: RelatedDocuments = related_documents(ArchivoAdjuntoTicket)


class TrazaDeTicket(Base):

    __tablename__ = 'TrazaDeTickets'

    NU_traza: Id = generic_id()
    NU_correlativo: Mapped[int] = mapped_column(Integer, default=1)
    AF_actividad: CommonString = common_string(64)
    AF_descripcion: CommonString = common_string(1024)
    TI_fecha_actividad: CommonDatetime = common_datetime()
    BO_anulada: Mapped[bool] = mapped_column(Boolean, default=False)
    # Parents

    # ---- Ticket

    NU_ticket: Mapped[int] = mapped_column(ForeignKey('Tickets.NU_ticket'))
    ticket: Mapped[Ticket] = relationship(
        remote_side=[Ticket.NU_ticket],
        backref=backref('trazas', lazy='joined')
    )

    # ---- Done by

    AF_usuario_realizador: Mapped[str] = mapped_column(ForeignKey('Usuarios.AF_alias'))
    usuario_realizador: Mapped[Usuario] = relationship(
        remote_side=[Usuario.AF_alias],
        backref=backref('trazas_de_ticket', lazy='joined')
    )

    # ---- Attached Files
    documentos_adjuntos: RelatedDocuments = related_documents(ArchivoAdjuntoTraza)