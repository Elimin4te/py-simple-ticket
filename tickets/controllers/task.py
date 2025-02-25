from shared.controllers.audited import AuditedModelController

from tickets.models import TrazaDeTicket
from tickets.controllers.ticket import TicketController

from auth.controllers.user import UserController

from flask import request, render_template
from flask_login import login_required, current_user

from flask_wtf import FlaskForm
from wtforms import BooleanField

from shared.views import ListView, FormView
from shared.engine import session
from shared.forms import required_string, required_int, format_obj_dates

from dateparser import parse

TASK_LIST_URL = '/tasks'
TASK_ADD_URL = '/tasks/add'
TASK_EDIT_URL = '/tasks/edit'

class TaskController(AuditedModelController[TrazaDeTicket]):
    
    model = TrazaDeTicket
    model_pk_field = 'NU_traza'


class TaskValidationForm(FlaskForm):
    AF_actividad = required_string("Nombre")
    AF_descripcion = required_string("Descripción")
    TI_fecha_actividad = required_string("Fecha de Actividad")
    BO_anulada = BooleanField("¿Anulada?")
    NU_ticket = required_int("Ticket")
    AF_usuario_realizador = required_string("Usuario Realizador")


class TaskListView(ListView):
    decorators = [login_required]

    list_title = "Listado de Actividades"
    page_title = "Actividades"
    search_option_placeholder = "Buscar por número de ticket..."
    active_menu_item = "tasks"

    controller = TaskController(session)
    url = TASK_LIST_URL

    def get_action_buttons_html(self) -> str:
        return render_template('task/action-buttons.html')

    def get_list_html(self) -> str:

        filter_set = {}
        filter_set['BO_anulada'] = 'BO_anulada' in request.args
        self.list_title = f'{self.list_title} {"(Anuladas)" if filter_set["BO_anulada"] else ""}' 

        search_str = request.args.get('search')
        if search_str:
            filter_set['NU_ticket'] = search_str

        objects = self.controller.filter(
            order_by=('NU_ticket', 'NU_correlativo'), 
            **filter_set
        )

        if len(objects) == 0:
            return None

        for obj in objects: format_obj_dates(obj, "%Y-%m-%d")

        return render_template(
            'task/list.html', objects=objects, edit_url=TASK_EDIT_URL
        )


class TaskCreateView(FormView):

    validation_form = TaskValidationForm
    form_title = "Crear Traza de Ticket"
    page_title = "Actividades"
    active_menu_item = "tasks"

    controller = TaskController(session, current_user)
    url = TASK_ADD_URL
    redirect_to = TASK_LIST_URL

    def get_correlative_for_instance(self, ticket_no):
        ticket_traces = self.controller.filter(NU_ticket=ticket_no)
        length = len(ticket_traces)
        return length + 1

    def on_valid(self):
        creation_kwargs = self.form_data
        creation_kwargs['NU_correlativo'] = self.get_correlative_for_instance(
            creation_kwargs.get('NU_ticket')
        )
        creation_kwargs['TI_fecha_actividad'] = parse(
            creation_kwargs.get('TI_fecha_actividad')
        )
        instance = TrazaDeTicket(**creation_kwargs)
        self.controller.create(instance)

    def get_form_html(self) -> str:

        # Load required FKs
        tickets = ()
        analists = UserController(session).filter(AF_codigo_rol="ASPR", BO_activo=True)
        incoming_ticket = request.args.get('ticket')

        if incoming_ticket:
            incoming_ticket = TicketController(session).get(incoming_ticket)
            self.form_title = f'{self.form_title} #{incoming_ticket.NU_ticket}'

        if self.edit_mode:
            incoming_ticket = None

        else:
            tickets = TicketController(session).filter(order_by="NU_ticket", BO_archivado=False)

        return render_template(
            "task/form.html",
            incoming_ticket = incoming_ticket,
            tickets  = tickets,
            analists = analists,
            obj = self.instance,
            edit_mode = self.edit_mode
        )


class TaskEditView(TaskCreateView):

    url = TASK_EDIT_URL
    edit_mode = True
    back_button = True

    instance: TrazaDeTicket = None

    def on_valid(self):
        updating_kwargs = {} | self.form_data
        updating_kwargs['TI_fecha_actividad'] = parse(
            updating_kwargs.get('TI_fecha_actividad')
        )
        self.controller.update(self.instance, **updating_kwargs)

    def get_form_html(self) -> str:
        self.form_title = f'Editar Traza #{self.instance.NU_correlativo} de Ticket #{self.instance.NU_ticket}'
        return super().get_form_html()