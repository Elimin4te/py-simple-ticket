from typing import TypeAlias
from shared.database import Base, ArchivableMixin, IsActiveMixin

from configuration.settings import TIMEZONE
from datetime import datetime

_ArchivableModel: TypeAlias = Base[ArchivableMixin]
_DisabableModel: TypeAlias = Base[IsActiveMixin]

class ArchiveActionMixin:

    def archive_instance(self, instance: _ArchivableModel, reason: str):
        return self.update(
            instance, 
            BO_archivado=True, 
            TI_fecha_archivado=datetime.now(TIMEZONE), 
            AF_motivo_archivado=reason
        )

    def unarchive_instance(self, instance: _ArchivableModel):
        return self.update(
            instance, 
            BO_archivado=False, 
            TI_fecha_archivado=None, 
            AF_motivo_archivado=None
        )


class DisableActionMixin:

    def disable_instance(self, instance: _DisabableModel):
        return self.update(instance, BO_activo=False)