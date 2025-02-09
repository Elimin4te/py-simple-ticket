from shared.controllers.audited import AuditedModelController
from auth.models.role import Rol

class RoleController(AuditedModelController):

    model = Rol
    model_pk_field = 'AF_codigo'