from shared.controllers.audited import AuditedModelController
from shared.controllers.mixins import ArchiveActionMixin

from tickets.models import Ticket, Prioridad
from tickets.models.ticket import STATUS_OPTS

from auth.models import Usuario
from auth.controllers.user import UserController

from tickets.controllers.priority import PriorityController
from tickets.controllers.incidence import IncidenceController
from tickets.controllers.category import CategoryController

from datetime import datetime
from configuration.settings import TIMEZONE

from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, SelectField

from flask import request, render_template
from flask_login import login_required, current_user

from shared.views import ListView, FormView, handle_archiving
from shared.forms import required_string, ArchivableFormMixin, format_obj_dates, sanitize_url_filter
from shared.engine import session

TICKET_LIST_URL = '/tickets'
TICKET_ADD_URL = '/tickets/add'
TICKET_DETAIL_URL = '/tickets/detail'

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

    controller = TicketController(session)
    url = TICKET_LIST_URL

    def get_action_buttons_html(self) -> str:
        categories = CategoryController(session).filter(BO_activo=True)
        analists   = UserController(session).filter(AF_codigo_rol="ASPR", BO_activo=True)
        return render_template(
            'ticket/action-buttons.html', 
            statuses=STATUS_OPTS,
            categories=categories,
            analists=analists
        )

    def get_list_html(self) -> str:

        # Sanitize filters
        
        filter_set = {'BO_archivado': False}
        filter_set.update(sanitize_url_filter(Ticket, request))
        search_str = request.args.get('search') or ''
        objects = self.controller.filter(
            Ticket.AF_titulo.ilike('%'+search_str+'%'), 
            order_by='NU_ticket', 
            **filter_set
        )
        if len(objects) == 0: return None

        for obj in objects: format_obj_dates(obj)
        return render_template(
            'ticket/list.html', objects=objects, ticket_detail_url=TICKET_DETAIL_URL
        )


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

        creation_kwargs = self.form_data
        if self.form_data.get('AF_analista_asignado'):
            creation_kwargs['TI_fecha_asignacion'] = datetime.now(TIMEZONE)

        instance = Ticket(**creation_kwargs)
        self.controller.create(instance)

    def get_form_html(self) -> str:

        # Load required FKs
        priorities = PriorityController(session).all()
        
        incidences = ()
        incoming_incidence = request.args.get('incidence')

        if incoming_incidence:
            incoming_incidence = IncidenceController(session).get(incoming_incidence)

        else:
            incidences = IncidenceController(session).all('NU_incidencia', 'AF_estatus')
            incidences = tuple(filter(lambda i: not i.BO_archivado and not i.has_ticket, incidences))

        categories = CategoryController(session).filter(BO_activo=True)
        analists   = UserController(session).filter(AF_codigo_rol="ASPR", BO_activo=True)

        return render_template(
            "ticket/form.html",
            incoming_incidence = incoming_incidence,
            priorities = priorities,
            incidences = incidences,
            categories = categories,
            analists   = analists
        )


class TicketDetailView(TicketCreateView):

    form_title = "Detalle de Ticket"

    edit_mode = True
    back_button = True
    url = TICKET_DETAIL_URL
    redirect_to = TICKET_LIST_URL

    instance: Ticket = None

    def on_valid(self):

        update_kwargs = self.form_data
        if self.form_data.get('AF_analista_asignado'):
            if self.form_data.get('AF_analista_asignado') != self.instance.AF_analista_asignado:
                update_kwargs['TI_fecha_asignacion'] = datetime.now(TIMEZONE)
        else:
            update_kwargs['TI_fecha_asignacion'] = None

        handle_archiving(self)

        self.controller.update(self.instance, **update_kwargs)

    def get_form_html(self) -> str:

        self.form_title = f'{self.form_title} - #{self.instance.NU_ticket}'

        # Load required FKs
        priorities = PriorityController(session).all()
        incidences = IncidenceController(session).all('NU_incidencia')
        incidences = tuple(filter(lambda i: not i.BO_archivado and not i.has_ticket, incidences))

        categories = CategoryController(session).filter(BO_activo=True)
        analists   = UserController(session).filter(AF_codigo_rol="ASPR", BO_activo=True)

        # Copy the instance to ensure coherence
        obj = self.instance
        format_obj_dates(obj)         

        return render_template(
            "ticket/detail-form.html",
            obj        = obj,
            statuses   = STATUS_OPTS,
            priorities = priorities,
            incidences = incidences,
            categories = categories,
            analists   = analists
        )