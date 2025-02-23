from shared.controllers.audited import AuditedModelController
from shared.controllers.mixins import ArchiveActionMixin

from tickets.models import Ticket
from tickets.models.ticket import STATUS_OPTS

from auth.models import Usuario
from auth.controllers.user import UserController

from tickets.controllers.priority import PriorityController
from tickets.controllers.incidence import IncidenceController
from tickets.controllers.category import CategoryController


from datetime import datetime
from configuration.settings import TIMEZONE

from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, SelectField, BooleanField

from flask import request, render_template, redirect
from flask_login import login_required, current_user

from shared.views import ListView, FormView
from shared.forms import required_string, ArchivableFormMixin
from shared.engine import session

TICKET_LIST_URL = '/tickets'
TICKET_ADD_URL = '/tickets/add'

class TicketController(AuditedModelController[Ticket], ArchiveActionMixin):
    
    model = Ticket
    model_pk_field = 'NU_ticket'

    def assign_technician(self, instance: Ticket, technician: Usuario):

        return self.update(
            instance, 
            AF_analista_asignado=technician.AF_alias, 
            TI_fecha_asignacion=datetime.now(tz=TIMEZONE)
        )

    def change_status(self, instance: Ticket, status: str):

        ### Notificacion automatica...

        return self.update(instance, AF_estatus=status)


class TicketValidationForm(FlaskForm, ArchivableFormMixin):
    NU_ticket = IntegerField("Número de Ticket")
    AF_titulo = required_string("Título")
    AF_descripcion = required_string("Descripción")
    AF_estatus = SelectField("Estatus", choices=STATUS_OPTS)
    NU_incidencia = required_string("Incidencia")
    AF_codigo_categoria = required_string("Categoría")
    AF_codigo_prioridad = required_string("Prioridad")
    AF_analista_asignado = StringField("Analista de Soporte")


class TicketListView(ListView):
    decorators = [login_required]

    list_html = ""
    list_title = "Listado de Tickets"
    page_title = "Tickets"
    search_option_placeholder = "Buscar por título..."
    active_menu_item = "tickets"
    force_empty = True

    controller = TicketController(session)
    url = TICKET_LIST_URL


class TicketCreateView(FormView):

    validation_form = TicketValidationForm
    form_title = "Crear Ticket"
    page_title = "Tickets"
    active_menu_item = "tickets"

    methods = "GET", "POST"
    controller = TicketController(session, current_user)
    url = TICKET_ADD_URL
    redirect_to = TICKET_LIST_URL

    def on_valid(self):
        instance = Ticket(**self.form_data)
        self.controller.create(instance)

    def get_form_html(self) -> str:

        # Load required FKs
        priorities = PriorityController(session).all()
        incidences = IncidenceController(session).all('NU_incidencia')
        incidences = tuple(filter(lambda i: not i.BO_archivado and not i.has_ticket, incidences))
        categories = CategoryController(session).filter(BO_activo=True)
        analists   = UserController(session).filter(AF_codigo_rol="ASPR", BO_activo=True)

        return render_template(
            "ticket/form.html",
            priorities = priorities,
            incidences = incidences,
            categories = categories,
            analists   = analists
        )

