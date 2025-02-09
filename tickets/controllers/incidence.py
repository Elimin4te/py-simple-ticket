from shared.controllers.audited import AuditedModelController
from tickets.models import Incidencia

class IncidenceController(AuditedModelController):
    
    model = Incidencia
    model_pk_field = 'NU_incidencia'




