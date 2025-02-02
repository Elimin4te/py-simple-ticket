from sqlalchemy import String, Integer, Enum, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship, backref

from shared.database import (
    Base,
    ArchivableMixin, 
    NullableDatetime, 
    nullable_datetime,
    Id,
    generic_id
)

from datetime import datetime
from configuration.settings import TIMEZONE

from tickets.models.category import Category
from tickets.models.priority import Priority
from tickets.models.incidence import Incidence

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

    id: Id = generic_id('NU_ticket')

    title: Mapped[str] = mapped_column(
        String(128),
        name = 'AF_titulo'
    )

    description: Mapped[str] = mapped_column(
        String(5096),
        name = 'AF_descripcion'
    )

    assigned_at: NullableDatetime = nullable_datetime('TI_fecha_asignacion')

    solved_at: NullableDatetime = nullable_datetime('TI_fecha_resolucion')

    # Parents

    # ---- Incidence

    incidence_id: Mapped[int] = mapped_column(
        ForeignKey('Incidencias.NU_incidencia'),
        name='NU_incidencia',
        unique=True
    )
    
    incidence: Mapped[Incidence] = relationship(
        remote_side=[Incidence.id],
        backref=backref('ticket', lazy='joined')
    )

    # ---- Category

    category_code: Mapped[str] = mapped_column(
        ForeignKey('Categorias.AF_codigo'),
        name='AF_codigo_categoria'
    )

    category: Mapped[Category] = relationship(
        remote_side=[Category.code],
        backref=backref('tickets', lazy='joined')
    )

    # ---- Priority

    priority_code: Mapped[str] = mapped_column(
        ForeignKey('Prioridades.AF_codigo'),
        name='AF_codigo_prioridad'
    )

    priority: Mapped[Priority] = relationship(
        remote_side=[Priority.code],
        backref=backref('tickets', lazy='joined')
    )

    # ---- Assigned User

    assigned_to_user_alias: Mapped[str] = mapped_column(
        ForeignKey('Usuarios.AF_alias'),
        name='AF_analista_asignado'
    )

    assigned_to: Mapped[User] = relationship(
        remote_side=[User.alias],
        backref=backref('assigned_tickets', lazy='joined')
    )


class TicketTrace(Base):

    __tablename__ = 'TrazaDeTickets'

    id: Id = generic_id('NU_traza')

    correlative: Mapped[int] = mapped_column(
        Integer,
        name="NU_correlativo",
        default=1
    )

    activity_title: Mapped[str] = mapped_column(
        String(64),
        name="AF_actividad"
    )

    description: Mapped[str] = mapped_column(
        String(128),
        name="AF_descripcion"
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        name='TI_fecha_actividad',
        default=datetime.now(tz=TIMEZONE)
    )

    is_canceled: Mapped[bool] = mapped_column(
        Boolean,
        name='BO_anulada',
        default=False
    )

    # Parents

    # ---- Ticket

    ticket_id: Mapped[int] = mapped_column(
        ForeignKey('Tickets.NU_ticket'),
        name='NU_ticket'
    )

    ticket: Mapped[Ticket] = relationship(
        remote_side=[Ticket.id],
        backref=backref('traces', lazy='joined')
    )

    # ---- Done by

    done_by_user_alias: Mapped[str] = mapped_column(
        ForeignKey('Usuarios.AF_alias'),
        name='AF_usuario_realizador'
    )

    done_by: Mapped[User] = relationship(
        remote_side=[User.alias],
        backref=backref('ticket_traces', lazy='joined')
    )