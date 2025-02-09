from shared.controllers.audited import AuditedModelController
from shared.controllers.mixins import ArchiveActionMixin

from tickets.models import Ticket
from auth.models import Usuario

from datetime import datetime
from configuration.settings import TIMEZONE

class TicketController(AuditedModelController[Ticket], ArchiveActionMixin):
    
    model = Ticket
    model_pk_field = 'NU_ticket'

    def assign_technician(self, instance: Ticket, technician: Usuario):

        return self.update(
            instance, 
            AF_analista_asignado=technician.AF_alias, 
            TI_fecha_asignacion=datetime.now(tz=TIMEZONE)
        )

    def change_status(self, instance: Ticket, status: str):

        ### Notificacion automatica...

        return self.update(instance, AF_estatus=status)
