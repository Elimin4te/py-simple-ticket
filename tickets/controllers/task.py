from shared.controllers.audited import AuditedModelController

from tickets.models import TrazaDeTicket

from flask_login import login_required
from shared.views import ListView
from shared.engine import session

TASK_LIST_URL = '/tasks'
TASK_ADD_URL = '/tasks/add'

class TaskController(AuditedModelController[TrazaDeTicket]):
    
    model = TrazaDeTicket
    model_pk_field = 'NU_traza'


class TaskListView(ListView):
    decorators = [login_required]

    list_html = ""
    list_title = "Listado de Actividades"
    page_title = "Actividades"
    search_option_placeholder = "Buscar por descripción..."
    active_menu_item = "tasks"
    force_empty = True

    controller = TaskController(session)
    url = TASK_LIST_URL