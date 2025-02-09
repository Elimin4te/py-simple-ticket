from shared.controllers.audited import AuditedModelController
from shared.controllers.mixins import DisableActionMixin

from tickets.models import Categoria

class CategoryController(AuditedModelController[Categoria], DisableActionMixin):
    
    model = Categoria
    model_pk_field = 'AF_codigo'

