from shared.controllers.audited import AuditedModelController
from shared.controllers.mixins import DisableActionMixin
from auth.models.role import Rol

class RoleController(AuditedModelController[Rol], DisableActionMixin):

    model = Rol
    model_pk_field = 'AF_codigo'