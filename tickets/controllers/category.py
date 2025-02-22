from shared.controllers.audited import AuditedModelController
from shared.controllers.mixins import DisableActionMixin

from tickets.models import Categoria

from flask_login import login_required
from shared.views import ListView
from shared.engine import session

CATEGORY_LIST_URL = '/categories'
CATEGORY_ADD_URL = '/categories/add'

class CategoryController(AuditedModelController[Categoria], DisableActionMixin):
    
    model = Categoria
    model_pk_field = 'AF_codigo'

class CategoryListView(ListView):
    decorators = [login_required]

    list_html = ""
    list_title = "Categorias"
    active_menu_item = "categories"
    hide_search_bar = True
    force_empty = True

    controller = CategoryController(session)
    url = CATEGORY_LIST_URL