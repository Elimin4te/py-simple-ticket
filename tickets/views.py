from flask.blueprints import Blueprint

from configuration import INDEX_URL
from shared.menu import app_menu, MenuEntry, MenuChild

from tickets.controllers.incidence import (
    IncidenceListView
)
from tickets.controllers.ticket import (
    TicketListView,
    TicketCreateView
)
from tickets.controllers.task import (
    TaskListView
)
from tickets.controllers.priority import (
    PriorityListView, 
    PriorityCreateView, 
    PriorityEditView
)
from tickets.controllers.category import (
    CategoryListView
)

tickets_bp = Blueprint('tickets', __name__, template_folder='templates')

# --------- URL Registries

IncidenceListView().register_in_app(tickets_bp)

TicketListView().register_in_app(tickets_bp)
TicketCreateView().register_in_app(tickets_bp)

TaskListView().register_in_app(tickets_bp)

PriorityListView().register_in_app(tickets_bp)
PriorityCreateView().register_in_app(tickets_bp)
PriorityEditView().register_in_app(tickets_bp)

CategoryListView().register_in_app(tickets_bp)

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
            MenuChild("Listado", TicketListView.url),
            MenuChild("Crear", TicketCreateView.url)
        )
    )
)

app_menu.add_entry(
    MenuEntry(
        'priorities',
        'Prioridades',
        'fa-exclamation-circle',
        breadcrumbs='soporte.tickets.prioridades',
        position=40,
        childs=(
            MenuChild("Listado", PriorityListView.url),
            MenuChild("Crear", PriorityCreateView.url),
        )
    )
)

app_menu.add_entry(
    MenuEntry(
        'add_ticket',
        'Crear Ticket',
        'fa-plus',
        TicketCreateView.url,
        'soporte.tickets',
        20
    )
)

app_menu.add_entry(
    MenuEntry(
        'categories',
        'Categorías',
        'fa-list-alt',
        breadcrumbs='soporte.tickets.categorias',
        position=50,
        childs=(
            MenuChild("Listado", CategoryListView.url),
            MenuChild("Crear", INDEX_URL)
        )
    )
)

app_menu.add_entry(
    MenuEntry(
        'tasks',
        'Actividades',
        'fa-tasks',
        breadcrumbs='soporte.tickets.actividades',
        position=60,
        childs=(
            MenuChild("Listado", TaskListView.url),
            MenuChild("Crear", INDEX_URL)
        )
    )
)
