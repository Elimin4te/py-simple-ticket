from flask import redirect, url_for, request
from flask.blueprints import Blueprint
from flask.views import MethodView
from flask.templating import render_template

from flask_login import current_user, login_required

from configuration import INDEX_URL, LOGIN_VIEW
from shared.views import render_into_index
from shared.menu import app_menu, MenuEntry
from shared.engine import session

from tickets.controllers.incidence import Incidencia, IncidenceController

tickets_bp = Blueprint('tickets', __name__, template_folder='templates')

TICKET_LIST_URL = '/tickets'
TICKET_ADD_URL = '/tickets/add'
TASK_LIST_URL = '/tasks'
INCIDENCE_DETAIL_URL = '/incidences/detail'

class IncidenceView(MethodView):

    decorators = [login_required]
    controller = IncidenceController(session)

    def get(self):

        with_ticket = 'with_ticket' in request.args.keys()
        without_ticket = 'without_ticket' in request.args.keys()
        all_incidences = not(with_ticket or without_ticket)
        search_params = request.args.get('search')

        filtering_kwargs = {}
        filtering_args = []

        if not all_incidences:
            filtering_kwargs['has_ticket'] = True if with_ticket else False

        if search_params:
            filtering_args.append(Incidencia.AF_descripcion.like("%" + search_params + "%"))

        incidence_list = self.controller.filter(*filtering_args, **filtering_kwargs)

        content = render_template(
            'incidences.html', 
            incidences=incidence_list, 
            is_empty=len(incidence_list) == 0,
            incidence_detail_url=INCIDENCE_DETAIL_URL
        )
        return render_into_index(content, "Incidencias", "incidences")


tickets_bp.add_url_rule(
    INDEX_URL,
    view_func=IncidenceView.as_view(LOGIN_VIEW),
    methods=["GET"],
)

app_menu.add_entry(MenuEntry('incidences', 'Incidencias', 'fa-bell', INDEX_URL, 'soporte.incidencias', 10))
app_menu.add_entry(MenuEntry('tickets', 'Tickets', 'fa-wrench', TICKET_LIST_URL, 'soporte.tickets', 20))
app_menu.add_entry(MenuEntry('add_ticket', 'Crear Ticket', 'fa-plus', TICKET_ADD_URL, 'soporte.tickets', 30))
app_menu.add_entry(MenuEntry('activities', 'Actividades', 'fa-tasks', TASK_LIST_URL, 'soporte.tickets.actividades', 40))

