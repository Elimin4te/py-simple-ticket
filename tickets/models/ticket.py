from sqlalchemy import Integer, Enum, ForeignKey, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship, backref

from shared.database import (
    Base,
    ArchivableMixin, 
    Id, generic_id,
    NullableDatetime, nullable_datetime,
    CommonString, common_string,
    CommonDatetime, common_datetime
)

from tickets.models.category import Categoria
from tickets.models.priority import Prioridad
from tickets.models.incidence import Incidencia

from auth.models.user import User


ESTATUS = Enum(
    "Nuevo",
    "Asignado",
    "En Curso",
    "Resuelto",
    "Cerrado",
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
        remote_side=[Prioridad.code],
        backref=backref('tickets', lazy='joined')
    )

    # ---- Assigned User

    AF_analista_asignado: Mapped[str] = mapped_column(ForeignKey('Usuarios.AF_alias'))
    analista_asignado: Mapped[User] = relationship(
        remote_side=[User.alias],
        backref=backref('assigned_tickets', lazy='joined')
    )


class TrazaDeTicket(Base):

    __tablename__ = 'TrazaDeTickets'

    NU_traza: Id = generic_id()
    NU_correlativo: Mapped[int] = mapped_column(Integer, default=1)
    AF_actividad: CommonString = common_string(64)
    AF_descripcion: CommonString = common_string(128)
    TI_fecha_actividad: CommonDatetime = common_datetime()
    BO_anulada: Mapped[bool] = mapped_column(Boolean, default=False)
    # Parents

    # ---- Ticket

    NU_ticket: Mapped[int] = mapped_column(ForeignKey('Tickets.NU_ticket'))
    ticket: Mapped[Ticket] = relationship(
        remote_side=[Ticket.id],
        backref=backref('trazas', lazy='joined')
    )

    # ---- Done by

    AF_usuario_realizador: Mapped[str] = mapped_column(ForeignKey('Usuarios.AF_alias'))
    usuario_realizador: Mapped[User] = relationship(
        remote_side=[User.alias],
        backref=backref('trazas_de_ticket', lazy='joined')
    )