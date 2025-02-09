from shared.controllers.audited import AuditedModelController
from tickets.models import Prioridad

class PriorityController(AuditedModelController):
    
    model = Prioridad
    model_pk_field = 'AF_codigo'