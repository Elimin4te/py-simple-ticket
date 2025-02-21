from flask import redirect, url_for, request
from flask.blueprints import Blueprint
from flask.templating import render_template

from flask_login import current_user, login_required

from configuration import INDEX_URL
from shared.views import ListView
from shared.menu import app_menu, MenuEntry, MenuChild
from shared.engine import session

from tickets.controllers.incidence import Incidencia, IncidenceController
from tickets.controllers.priority import PriorityListView, PriorityCreateView

tickets_bp = Blueprint('tickets', __name__, template_folder='templates')

TICKET_LIST_URL = '/tickets'
TICKET_ADD_URL = '/tickets/add'
TASK_LIST_URL = '/tasks'
TASK_ADD_URL = '/tasks/add'
INCIDENCE_DETAIL_URL = '/incidences/detail'
PRIORITY_LIST_URL = '/priorities'
PRIORITY_ADD_URL = '/priorities/add'

# --------- View Controllers

class IncidenceListView(ListView):

    decorators = [login_required]
    controller = IncidenceController(session)

    list_title = "Listado de Incidencias"
    page_title = "Incidencias"
    active_menu_item = "incidences"

    def get_action_buttons_html(self) -> str:
        return render_template("incidence/action-buttons.html")

    def get_list_html(self):

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
        if len(incidence_list) == 0:
            return None

        content = render_template(
            'incidence/list.html', 
            incidences=incidence_list,
            incidence_detail_url=INCIDENCE_DETAIL_URL
        )

        return content


class TicketListView(ListView):
    decorators = [login_required]

    list_html = ""
    list_title = "Listado de Tickets"
    page_title = "Tickets"
    search_option_placeholder= "Buscar por título..."
    active_menu_item = "tickets"
    force_empty = True


class TaskListView(ListView):
    decorators = [login_required]

    list_html = ""
    list_title = "Listado de Actividades"
    page_title = "Actividades"
    search_option_placeholder= "Buscar por número de ticket..."
    active_menu_item = "tasks"
    force_empty = True


# --------- URLs

tickets_bp.add_url_rule(
    INDEX_URL,
    view_func=IncidenceListView.as_view('incidence-list-view'),
    methods=["GET"],
)

tickets_bp.add_url_rule(
    TICKET_LIST_URL,
    view_func=TicketListView.as_view('ticket-list-view'),
    methods=["GET"],
)

tickets_bp.add_url_rule(
    TASK_LIST_URL,
    view_func=TaskListView.as_view('task-list-view'),
    methods=["GET"],
)

tickets_bp.add_url_rule(
    PRIORITY_LIST_URL,
    view_func=PriorityListView.as_view('priority-list-view'),
    methods=["GET"],
)

tickets_bp.add_url_rule(
    PRIORITY_ADD_URL,
    view_func=PriorityCreateView.as_view('priority-add-view'),
    methods=["GET", "POST"]
)

# --------- Menu Entries

app_menu.add_entry(
    MenuEntry(
        'incidences', 
        'Incidencias', 
        'fa-bell', 
        INDEX_URL, 
        'soporte.incidencias', 
        10
    )
)

app_menu.add_entry(
    MenuEntry(
        'tickets', 
        'Tickets', 
        'fa-wrench',
        breadcrumbs='soporte.tickets',
        position=30,
        childs=(
            MenuChild("Listado", TICKET_LIST_URL),
            MenuChild("Crear", TICKET_ADD_URL),
            MenuChild("Prioridades", PRIORITY_LIST_URL)
        )
    )
)

app_menu.add_entry(
    MenuEntry(
        'add_ticket', 
        'Crear Ticket', 
        'fa-plus',
        TICKET_ADD_URL, 
        'soporte.tickets', 
        20
    )
)

app_menu.add_entry(
    MenuEntry(
        'tasks', 
        'Actividades', 
        'fa-tasks',
        breadcrumbs='soporte.tickets.actividades', 
        position=40,
        childs=(
            MenuChild("Listado", TASK_LIST_URL),
            MenuChild("Crear", TASK_ADD_URL)
        )
    )
)

